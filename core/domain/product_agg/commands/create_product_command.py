from typing import List

from pydantic import BaseModel, Field


class CreateProductCommand(BaseModel):
    name: str = Field(alias='name')
    ean: str = Field(alias='ean')
    description: str = Field(alias='description')
    images: List[str] = Field(alias='images')
    price: int = Field(alias='price')
    quantity: int = Field(alias='quantity')
