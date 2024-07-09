from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import AfterValidator, BaseModel, Field, model_validator
from store.schemas.base import BaseSchemaMixin, OutMixin


class ProductBase(BaseModel):
    # os 3 poninhos reforçam pro pydantics que esses atributos são obrigatórios
    name: Optional[str] = Field(None, description="Product name")
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")

    def get_class_variables(cls):
        return [
            nome
            for nome, valor in vars(cls).items()
            if not callable(valor) and not nome.startswith("__")
        ]


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn, OutMixin):
    ...


def convert_decimal_128(v):
    return Decimal128(str(v))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")


class ProductUpdateOut(ProductOut):
    @model_validator(mode="before")
    def update_timestamp(cls, values):
        values["updated_at"] = datetime.utcnow()
        return values
