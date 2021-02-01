from unittest import TestCase

from faker import Faker

from core.domain.product_agg.enums.enums import ProductStatus
from core.infrastructure.mapping.product_profile import ProductProfile


class ProductProfileTest(TestCase):

    def setUp(self) -> None:
        self.faker = Faker()
        self.profile = ProductProfile()

        self.data = {
            'id': self.faker.name(),
            'name': self.faker.name(),
            'ean': self.faker.ean(length=13),
            'description': self.faker.text(),
            'images': [self.faker.image_url()],
            'price': self.faker.pyint(),
            'quantity': self.faker.pyint(),
            'status': self.faker.random_choices(list(ProductStatus), 1)[0].value,
            'created_at': self.faker.date_time(),
            'updated_at': self.faker.date_time(),
            'deleted_at': self.faker.date_time(),
        }

    def test_map_to_entity(self):
        product = self.profile.map_to_entity(self.data)

        self.assertEqual(product.id_, self.data['id'])
        self.assertEqual(product.name, self.data['name'])
        self.assertEqual(product.ean, self.data['ean'])
        self.assertEqual(product.description, self.data['description'])
        self.assertEqual(product.images, self.data['images'])
        self.assertEqual(product.price, self.data['price'])
        self.assertEqual(product.quantity, self.data['quantity'])
        self.assertEqual(product.status, self.data['status'])
        self.assertEqual(product.created_at, self.data['created_at'])
        self.assertEqual(product.updated_at, self.data['updated_at'])
        self.assertEqual(product.deleted_at, self.data['deleted_at'])

    def test_map_to_data(self):
        product = self.profile.map_to_entity(self.data)
        data = self.profile.map_to_data(product)

        self.assertEqual(data['id_'], self.data['id'])
        self.assertEqual(data['name'], self.data['name'])
        self.assertEqual(data['ean'], self.data['ean'])
        self.assertEqual(data['description'], self.data['description'])
        self.assertEqual(data['images'], self.data['images'])
        self.assertEqual(data['price'], self.data['price'])
        self.assertEqual(data['quantity'], self.data['quantity'])
        self.assertEqual(data['status'], self.data['status'])
        self.assertEqual(data['created_at'], self.data['created_at'])
        self.assertEqual(data['updated_at'], self.data['updated_at'])
        self.assertEqual(data['deleted_at'], self.data['deleted_at'])
