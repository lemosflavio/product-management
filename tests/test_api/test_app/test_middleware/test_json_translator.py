from unittest import TestCase
from unittest.mock import MagicMock

from api.app.middleware.json_translator import JsonTranslatorMiddleware


class JsonTranslatorMiddlewareTest(TestCase):

    def setUp(self) -> None:
        self.middleware = JsonTranslatorMiddleware()
        self.request = MagicMock()
        self.response = MagicMock()

    def test_process_response(self):
        result = {}
        self.response.context.result = result

        self.middleware.process_response(self.request, self.response, None, None)

        self.assertEqual(self.response.body, '{}')

    def test_process_request(self):
        body = MagicMock()
        body.decode.return_value = '{}'
        self.request.bounded_stream.read.return_value = body

        self.middleware.process_request(self.request, self.response)
        self.assertEqual(self.request.context.doc, {})
