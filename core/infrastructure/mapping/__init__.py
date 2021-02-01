from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractProfile(ABC):

    @abstractmethod
    def map_to_entity(self, data: dict):
        pass

    @abstractmethod
    def map_to_data(self, entity: BaseModel):
        pass
