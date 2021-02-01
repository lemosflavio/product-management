from datetime import datetime
from unittest import TestCase

from faker import Faker

from core.domain.product_agg.commands.create_product_command import CreateProductCommand
from core.domain.product_agg.commands.update_product_command import UpdateProductCommand
from core.domain.product_agg.entities.product import Product
from core.domain.product_agg.enums.enums import ProductStatus


class ProductTest(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.command = CreateProductCommand(
            name=self.faker.name(),
            ean=self.faker.ean(length=13),
            description=self.faker.text(),
            images=[self.faker.image_url()],
            price=self.faker.pyint(),
            quantity=self.faker.pyint(),
        )
        self.product = Product.create(self.command)

    def test_create(self):
        now = datetime.utcnow()
        product = Product.create(self.command)

        self.assertEqual(product.name, self.command.name)
        self.assertEqual(product.ean, self.command.ean)
        self.assertEqual(product.description, self.command.description)
        self.assertEqual(product.images, self.command.images)
        self.assertEqual(product.price, self.command.price)
        self.assertEqual(product.quantity, self.command.quantity)
        self.assertEqual(product.status, ProductStatus.ACTIVE.value)
        self.assertGreaterEqual(product.created_at, now)
        self.assertIsNone(product.id_)
        self.assertIsNone(product.updated_at)
        self.assertIsNone(product.deleted_at)

    def test_update(self):
        now = datetime.utcnow()
        command = UpdateProductCommand(
            name=self.faker.name(),
            ean=self.faker.ean(length=13),
            description=self.faker.text(),
            images=[self.faker.image_url()],
            price=self.faker.pyint(),
            quantity=self.faker.pyint(),
        )
        self.product.update(command)

        self.assertEqual(self.product.name, command.name)
        self.assertEqual(self.product.ean, command.ean)
        self.assertEqual(self.product.description, command.description)
        self.assertEqual(self.product.images, command.images)
        self.assertEqual(self.product.price, command.price)
        self.assertEqual(self.product.quantity, command.quantity)
        self.assertGreaterEqual(self.product.updated_at, now)
        self.assertIsNone(self.product.deleted_at)

    def test_delete(self):
        now = datetime.utcnow()

        self.product.delete()

        self.assertEqual(self.product.status, ProductStatus.DELETED.value)
        self.assertGreaterEqual(self.product.deleted_at, now)

    def test_activate(self):
        now = datetime.utcnow()

        self.product.activate()

        self.assertEqual(self.product.status, ProductStatus.ACTIVE.value)
        self.assertGreaterEqual(self.product.updated_at, now)
