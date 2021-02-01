from logging import Logger

import falcon

from api.app.resources.abstract_resource import AbstractResource


class ProductResource(AbstractResource):
    search_fields = ['ean', 'status']

    def __init__(self, service, logger: Logger):
        self.service = service
        self.logger = logger

    def __get_search_params(self, req):
        search = {}
        for field in self.search_fields:
            param = req.get_param(field)
            if param:
                search[field] = param
        return search

    def on_get(self, req, resp, product_id: str = None):
        if product_id:
            result = self.service.find_one(product_id)
        else:
            search = self.__get_search_params(req)
            result = self.service.find(search)

        resp.context.result = result
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, product_id: str = None):
        try:
            doc = req.context.doc
        except AttributeError:
            raise falcon.HTTPBadRequest(
                title='Missing document',
                description='A document must be submitted in the request body.')

        result = self.service.create(doc)

        resp.status = falcon.HTTP_201
        resp.context.result = result
        resp.location = f'/products/{result.id_}'

    def on_put(self, req, resp, product_id: str):
        try:
            doc = req.context.doc
        except AttributeError:
            raise falcon.HTTPBadRequest(
                title='Missing document',
                description='A document must be submitted in the request body.')

        self.service.update_one(product_id, doc)

        resp.status = falcon.HTTP_202
        resp.location = f'/products/{product_id}'

    def on_delete(self, req, resp, product_id: str):

        self.service.delete(product_id)

        resp.status = falcon.HTTP_202
        resp.location = f'/products/'
