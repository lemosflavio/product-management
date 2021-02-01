import json

import falcon
from pydantic.main import BaseModel


class JsonTranslatorMiddleware:
    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return

        body = req.bounded_stream.read()
        if not body:
            raise falcon.HTTPBadRequest(
                title='Empty request body',
                description='A valid JSON document is required.'
            )

        try:
            req.context.doc = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):

            raise falcon.HTTPBadRequest(
                title='Malformed JSON',
                description='Could not decode the request body. The JSON was incorrect or not encoded as UTF-8.'
            )

    def process_response(self, req, resp, resource, req_succeeded):
        if not hasattr(resp.context, 'result'):
            return

        resp.body = json.dumps(resp.context.result, default=self.__json_default)

    @staticmethod
    def __json_default(obj):
        if isinstance(obj, BaseModel):
            return obj.dict()
        return
