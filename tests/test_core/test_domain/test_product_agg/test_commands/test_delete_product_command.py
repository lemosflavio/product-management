from unittest import TestCase

from pydantic import ValidationError

from core.domain.product_agg.commands.delete_product_command import DeleteProductCommand


class DeleteProductCommandTest(TestCase):

    def test_required_fields(self):
        with self.assertRaises(ValidationError) as exception:
            DeleteProductCommand()

        required_fields = [error._loc for error in exception.exception.raw_errors]
        self.assertIn('id', required_fields)
