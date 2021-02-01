from abc import ABC, abstractmethod
from typing import List


class AbstractDatabase(ABC):
    @abstractmethod
    def find_one(self, query: dict) -> dict:
        pass

    @abstractmethod
    def find(self, query: dict) -> List[dict]:
        pass

    @abstractmethod
    def update_one(self, query: dict, data: dict) -> dict:
        pass

    @abstractmethod
    def create(self, data: dict) -> dict:
        pass

    @abstractmethod
    def is_health(self) -> bool:
        pass
