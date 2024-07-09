from typing import List
from uuid import UUID

import pytest
from store.schemas.product import ProductIn, ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


from store.core.exceptions import InsertionException, NotFoundException


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Samsung A34 PRO"


async def test_usecases_create_should_return_fields_required(product_id, product_in):
    with pytest.raises(InsertionException) as err:
        await product_usecase.create(
            body=ProductIn(
                **{"name": "Samsung A34 PRO", "quantity": 1500}, id=product_id
            )
        )

    assert err.value.message == "Wrong Insertion: fields required ['name', 'quantity']"


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Samsung A34 PRO"


async def test_usecases_get_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID("002acf88-17b5-47f8-aa5c-97dc4f9d141b"))

    assert (
        err.value.message
        == "Product not found with filter: 002acf88-17b5-47f8-aa5c-97dc4f9d141b"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_up, product_inserted):
    product_up.price = "5.433"
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


async def test_usecases_delete_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID("002acf88-17b5-47f8-aa5c-97dc4f9d141b"))

    assert (
        err.value.message
        == "Product not found with filter: 002acf88-17b5-47f8-aa5c-97dc4f9d141b"
    )
