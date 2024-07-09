from typing import List
import pytest
from tests.factories import product_data
from fastapi import status


@pytest.mark.asyncio
async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())
    content = response.json()

    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Samsung A34 PRO",
        "quantity": 1500,
        "price": "4.800",
        "status": True,
    }


async def test_controller_usecases_create_should_return_conflict(client, products_url):
    response = await client.post(
        products_url, json={"name": "Samsung A34 PRO", "quantity": 1500}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": "Wrong Insertion: fields required ['name', 'quantity']"
    }


async def test_controller_usecases_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")
    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Samsung A34 PRO",
        "quantity": 1500,
        "price": "4.800",
        "status": True,
    }


async def test_controller_usecases_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}3ab98d3b-b8a0-47e2-a2fc-75569bce6618")

    response.status_code == status.HTTP_404_NOT_FOUND
    response.json() == {
        "detail": "Product not found with filter: 3ab98d3b-b8a0-47e2-a2fc-75569bce6618"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_usecases_query_should_return_success(client, products_url):
    response = await client.get(f"{products_url}")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_usecases_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "3.200"}
    )
    content = response.json()

    assert content["created_at"] != content["updated_at"]

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Samsung A34 PRO",
        "quantity": 1500,
        "price": "3.200",
        "status": True,
    }


async def test_controller_usecases_patch_should_return_not_found(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}3ab98d3b-b8a0-47e2-a2fc-75569bce6618", json={"price": "3.200"}
    )

    response.status_code == status.HTTP_404_NOT_FOUND
    response.json() == {
        "detail": "Product not found with filter: 3ab98d3b-b8a0-47e2-a2fc-75569bce6618"
    }


"""
async def test_controller_usecases_delete_should_return_no_content(client, products_url, product_inserted):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT"""


async def test_controller_usecases_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}3ab98d3b-b8a0-47e2-a2fc-75569bce6618"
    )

    response.status_code == status.HTTP_404_NOT_FOUND
    response.json() == {
        "detail": "Product not found with filter: 3ab98d3b-b8a0-47e2-a2fc-75569bce6618"
    }
