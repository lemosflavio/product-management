import falcon

from api.app.resources.abstract_resource import AbstractResource
from core.infrastructure.database import AbstractDatabase


class HealthCheckResource(AbstractResource):

    def __init__(self, database: AbstractDatabase):
        self.__database = database

    def on_get(self, req, resp) -> None:
        resp.status = falcon.HTTP_200
        resp.context.result = {'ok': self.__database.is_health()}

    def on_post(self, req, resp) -> None:
        raise falcon.HTTPMethodNotAllowed(title='Method not allowed', allowed_methods=["GET"])

    def on_put(self, req, resp) -> None:
        raise falcon.HTTPMethodNotAllowed(title='Method not allowed', allowed_methods=["GET"])

    def on_delete(self, req, resp) -> None:
        raise falcon.HTTPMethodNotAllowed(title='Method not allowed', allowed_methods=["GET"])
