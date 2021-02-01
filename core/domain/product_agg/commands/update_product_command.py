from typing import List, Optional

from pydantic import Field, BaseModel


class UpdateProductCommand(BaseModel):
    # id_: str = Field(alias='id')
    name: Optional[str] = Field(alias='name')
    ean: Optional[str] = Field(alias='ean')
    description: Optional[str] = Field(alias='description')
    images: Optional[List[str]] = Field(alias='images')
    price: Optional[int] = Field(alias='price')
    quantity: Optional[int] = Field(alias='quantity')
