from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from core.domain.product_agg.commands.create_product_command import CreateProductCommand
from core.domain.product_agg.commands.update_product_command import UpdateProductCommand
from core.domain.product_agg.enums.enums import ProductStatus


class Product(BaseModel):
    id_: str = Field(alias='id', default=None)
    name: str = Field(alias='name')
    ean: str = Field(alias='ean')
    description: str = Field(alias='description')
    images: List[str] = Field(alias='images')
    price: int = Field(alias='price')
    quantity: int = Field(alias='quantity')
    status: str = Field(alias='status', default=ProductStatus.ACTIVE.value)
    created_at: datetime = Field(alias='created_at', default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(alias='updated_at', default=None)
    deleted_at: Optional[datetime] = Field(alias='deleted_at', default=None)

    @classmethod
    def create(cls, command: CreateProductCommand):
        return cls(
            name=command.name,
            ean=command.ean,
            description=command.description,
            images=command.images,
            price=command.price,
            quantity=command.quantity,
        )

    def update(self, command: UpdateProductCommand):
        self.name = command.name or self.name
        self.ean = command.ean or self.ean
        self.description = command.description or self.description
        self.images = command.images or self.images
        self.price = command.price or self.price
        self.quantity = command.quantity or self.quantity
        self.updated_at = datetime.utcnow()

    def delete(self):
        self.status = ProductStatus.DELETED.value
        self.deleted_at = datetime.utcnow()

    def activate(self):
        self.status = ProductStatus.ACTIVE.value
        self.updated_at = datetime.utcnow()
