from unittest import TestCase

from core.domain.product_agg.commands.update_product_command import UpdateProductCommand


class UpdateProductCommandTest(TestCase):

    def test_non_required_fields(self):
        command = UpdateProductCommand()

        self.assertIsNone(command.name)
        self.assertIsNone(command.ean)
        self.assertIsNone(command.description)
        self.assertIsNone(command.images)
        self.assertIsNone(command.price)
        self.assertIsNone(command.quantity)
