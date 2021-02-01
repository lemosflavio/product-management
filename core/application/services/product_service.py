from core.domain.product_agg.commands.create_product_command import CreateProductCommand
from core.domain.product_agg.commands.update_product_command import UpdateProductCommand
from core.domain.product_agg.entities.product import Product
from core.domain.product_agg.enums.enums import ProductStatus
from core.infrastructure.repository.product_repository import ProductRepository


class ProductService:

    def __init__(self, repository: ProductRepository):
        self.__repo = repository

    def create(self, data: dict):
        product = self.__repo.find_one({'ean': data['ean']})

        if not product:
            command = CreateProductCommand(**data)
            product = Product.create(command)
            return self.__repo.create(product)

        if product.status == ProductStatus.DELETED.value:
            product.activate()
            self.__repo.update_one(product)
            return product

        return product

    def update_one(self, id_: str, data: dict):
        command = UpdateProductCommand(**data)

        product = self.__repo.find_one(query={'id': id_})

        if not product:
            return

        product.update(command)
        self.__repo.update_one(entity=product)

        return product

    def delete(self, id_: str):
        product = self.find_one(id_)

        if not product:
            return

        product.delete()
        self.__repo.update_one(entity=product)

        return product

    def find_one(self, id_: str):
        return self.__repo.find_one(query={'id': id_})

    def find(self, query: dict):
        return self.__repo.find(query=query)
