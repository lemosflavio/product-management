from unittest import TestCase

from pydantic import ValidationError

from core.domain.product_agg.commands.create_product_command import CreateProductCommand


class CreateProductCommandTest(TestCase):

    def test_required_fields(self):
        with self.assertRaises(ValidationError) as exception:
            CreateProductCommand()

        required_fields = [error._loc for error in exception.exception.raw_errors]
        self.assertIn('name', required_fields)
        self.assertIn('ean', required_fields)
        self.assertIn('description', required_fields)
        self.assertIn('images', required_fields)
        self.assertIn('price', required_fields)
        self.assertIn('quantity', required_fields)
