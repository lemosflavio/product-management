from unittest import TestCase
from unittest.mock import MagicMock, patch

from core.application.services.product_service import ProductService
from core.domain.product_agg.enums.enums import ProductStatus


class ProductServiceTest(TestCase):
    def setUp(self) -> None:
        self.repo = MagicMock()
        self.service = ProductService(self.repo)

    def test_find(self):
        query = {}

        self.service.find(query)

        self.repo.find.assert_called_once_with(query=query)

    def test_find_one(self):
        id_ = 'foo'
        self.service.find_one(id_)

        self.repo.find_one.assert_called_once_with(query={'id': id_})

    def test_delete(self):
        id_ = 'foo'
        product = MagicMock()
        self.repo.find_one.return_value = product

        self.service.delete(id_)

        self.repo.find_one.assert_called_once_with(query={'id': id_})
        product.delete.assert_called_once()
        self.repo.update_one.assert_called_once_with(entity=product)

    def test_dont_delete_if_not_exists(self):
        id_ = 'foo'
        self.repo.find_one.return_value = None

        self.service.delete(id_)

        self.repo.find_one.assert_called_once_with(query={'id': id_})
        self.repo.update_one.assert_not_called()

    @patch('core.application.services.product_service.UpdateProductCommand', autospec=True)
    def test_update_one(self, command):
        id_ = 'foo'
        data = {}
        product = MagicMock()
        self.repo.find_one.return_value = product
        self.service.update_one(id_, data)

        self.repo.find_one.assert_called_once_with(query={'id': id_})
        command.assert_called_once_with(**data)
        product.update.assert_called_once_with(command())
        self.repo.update_one.assert_called_once_with(entity=product)

    def test_dont_update_one_if_not_exists(self):
        id_ = 'foo'
        data = {}
        self.repo.find_one.return_value = None
        self.service.update_one(id_, data)

        self.repo.find_one.assert_called_once_with(query={'id': id_})
        self.repo.update_one.assert_not_called()

    @patch('core.application.services.product_service.CreateProductCommand', autospec=True)
    @patch('core.application.services.product_service.Product.create')
    def test_create(self, product_create_method, command):
        data = {'ean': 'foo'}
        self.repo.find_one.return_value = None
        product = MagicMock()
        product_create_method.return_value = product

        self.service.create(data)

        self.repo.find_one.assert_called_once_with({'ean': data['ean']})
        command.assert_called_once_with(**data)
        product_create_method.assert_called_once_with(command())
        self.repo.create.assert_called_once_with(product_create_method())

    def test_create_active_product_if_deleted(self):
        data = {'ean': 'foo'}
        product = MagicMock(status=ProductStatus.DELETED.value)

        self.repo.find_one.return_value = product

        self.service.create(data)

        self.repo.find_one.assert_called_once_with({'ean': data['ean']})
        self.repo.create.assert_not_called()
        product.activate.assert_called_once()
        self.repo.update_one.assert_called_once_with(product)
