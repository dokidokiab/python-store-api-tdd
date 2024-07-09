from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import UUID4
from store.core.exceptions import InsertionException, NotFoundException

from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body)
    except InsertionException as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message
        )


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def get(
    min_price: Optional[float] = Query(None, alias="minPrice", gt=0),
    max_price: Optional[float] = Query(None, alias="maxPrice", gt=0),
    usecase: ProductUsecase = Depends(),
) -> List[ProductOut]:
    if min_price is not None and max_price is not None:
        return await usecase.query_by_price_range(
            min_price=min_price, max_price=max_price
        )
    return await usecase.query()


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
