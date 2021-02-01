import falcon

from api.app.resources.abstract_resource import AbstractResource


class HealthCheckResource(AbstractResource):

    def on_get(self, req, resp) -> None:
        resp.status = falcon.HTTP_200
        resp.context.result = {'ok': True}

    def on_post(self, req, resp) -> None:
        raise falcon.HTTPMethodNotAllowed(title='Method not allowed', allowed_methods=["GET"])

    def on_put(self, req, resp) -> None:
        raise falcon.HTTPMethodNotAllowed(title='Method not allowed', allowed_methods=["GET"])

    def on_delete(self, req, resp) -> None:
        raise falcon.HTTPMethodNotAllowed(title='Method not allowed', allowed_methods=["GET"])
