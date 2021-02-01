from typing import List, Optional

from core.domain.product_agg.entities.product import Product
from core.infrastructure.database import AbstractDatabase
from core.infrastructure.mapping import AbstractProfile


class ProductRepository:
    def __init__(self, database: AbstractDatabase, profile: AbstractProfile):
        self.__database = database
        self.__profile = profile

    def map_to_entity(self, item: Optional[dict]) -> Product:
        return item and self.__profile.map_to_entity(item)

    def map_to_data(self, entity: Product) -> dict:
        return self.__profile.map_to_data(entity)

    def find_one(self, query: dict) -> Product:
        item = self.__database.find_one(query=query)
        return self.map_to_entity(item=item)

    def find(self, query: dict) -> List[Product]:
        items = self.__database.find(query=query)
        return [self.map_to_entity(item=item) for item in items]

    def update_one(self, entity) -> Product:
        query = {'id': entity.id_}
        data = self.map_to_data(entity)

        item = self.__database.update_one(query=query, data=data)

        return self.map_to_entity(item=item)

    def create(self, entity) -> Product:
        data = self.map_to_data(entity)
        item = self.__database.create(data)

        return self.map_to_entity(item=item)
