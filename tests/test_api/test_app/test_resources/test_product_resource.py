from unittest import TestCase
from unittest.mock import MagicMock

import falcon

from api.app.resources.product_resource import ProductResource


class ProductResourceTest(TestCase):

    def setUp(self) -> None:
        self.service = MagicMock()
        self.logger = MagicMock()

        self.request = MagicMock()
        self.response = MagicMock()

        self.resource = ProductResource(service=self.service, logger=self.logger)

    def test_on_get_with_find_one(self):
        product_id = 'product_id'
        result = MagicMock()
        self.service.find_one.return_value = result

        self.resource.on_get(self.request, self.response, product_id)

        self.service.find_one.assert_called_once_with(product_id)
        self.assertEqual(self.response.context.result, result)
        self.assertEqual(self.response.status, falcon.HTTP_200)

    def test_on_get_with_find(self):
        product_id = None
        result = MagicMock()
        search = {}
        self.request.get_param.return_value = {}
        self.service.find.return_value = result

        self.resource.on_get(self.request, self.response, product_id)

        self.service.find_one.assert_not_called()
        self.service.find.assert_called_once_with(search)
        self.assertEqual(self.response.context.result, result)
        self.assertEqual(self.response.status, falcon.HTTP_200)

    def test_on_post(self):
        result = MagicMock()
        self.request.context.doc = MagicMock()
        self.service.create.return_value = result

        self.resource.on_post(self.request, self.response)

        self.service.create.assert_called_once_with(self.request.context.doc)
        self.assertEqual(self.response.context.result, result)
        self.assertEqual(self.response.status, falcon.HTTP_201)

    def test_on_put(self):
        product_id = 'product_id'
        self.request.context.doc = MagicMock()

        self.resource.on_put(self.request, self.response, product_id)

        self.service.update_one.assert_called_once_with(product_id, self.request.context.doc)

        self.assertEqual(self.response.status, falcon.HTTP_202)
