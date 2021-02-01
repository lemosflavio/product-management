import logging
from wsgiref import simple_server

import falcon

from api.app.config import DATABASE_CONFIG, API_CONFIG
from api.app.exceptions.handlers.generic_exception_handler import GenericExceptionHandler
from api.app.middleware.json_translator import JsonTranslatorMiddleware
from api.app.middleware.require_json import RequireJsonMiddleware
from api.app.resources.health_check_resource import HealthCheckResource
from api.app.resources.product_resource import ProductResource
from core.application.services.product_service import ProductService
from core.infrastructure.database.mongo import MongoDB
from core.infrastructure.mapping.product_profile import ProductProfile
from core.infrastructure.repository.product_repository import ProductRepository


class Api(falcon.API):

    def __init__(self):
        super(Api, self).__init__(middleware=[
            RequireJsonMiddleware(),
            JsonTranslatorMiddleware(),
        ])
        self.__database = MongoDB(DATABASE_CONFIG)
        self.__logger = logging.getLogger(API_CONFIG.NAME)
        logging.basicConfig()
        self.__add_routes()
        self.__add_error_handlers()

    @property
    def __repositories(self):
        return {
            'product': ProductRepository(self.__database, ProductProfile()),
        }

    @property
    def __services(self):
        return {
            'product': ProductService(self.__repositories['product']),
        }

    @property
    def __resources(self):
        return {
            'product': ProductResource(self.__services['product'], self.__logger),
            'health_check': HealthCheckResource()
        }

    def __add_routes(self):
        self.add_route('/products/{product_id}', self.__resources['product'])
        self.add_route('/health_check', self.__resources['health_check'])
        self.add_route('/', self.__resources['health_check'])

    def __add_error_handlers(self):
        self.add_error_handler(Exception, GenericExceptionHandler(logger=self.__logger).handle)
        self.add_error_handler(falcon.HTTPNotFound, lambda *args, **kwargs: '')

    def start(self):
        httpd = simple_server.make_server(API_CONFIG.HOST, API_CONFIG.PORT, self)
        httpd.serve_forever()
