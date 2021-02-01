import abc


class AbstractResource(abc.ABC):

    @abc.abstractmethod
    def on_get(self, req, resp) -> None:
        pass

    @abc.abstractmethod
    def on_post(self, req, resp) -> None:
        pass

    @abc.abstractmethod
    def on_put(self, req, resp) -> None:
        pass

    @abc.abstractmethod
    def on_delete(self, req, resp) -> None:
        pass
