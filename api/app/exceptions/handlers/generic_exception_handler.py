from logging import Logger

import falcon


class GenericExceptionHandler:
    def __init__(self, logger: Logger):
        self.__logger = logger

    def handle(self, ex, req, resp, params):
        self.__logger.error('Error while handling request', exc_info=ex)
        raise falcon.HTTPInternalServerError()
