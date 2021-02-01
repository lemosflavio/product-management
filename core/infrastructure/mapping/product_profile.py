from core.domain.product_agg.entities.product import Product
from core.infrastructure.mapping import AbstractProfile


class ProductProfile(AbstractProfile):

    def map_to_entity(self, data):
        return Product(**data)

    def map_to_data(self, entity: Product):
        return entity.dict()
