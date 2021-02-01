from typing import List, Optional

from bson import ObjectId
from pydantic import BaseSettings
from pymongo import MongoClient

from core.infrastructure.database import AbstractDatabase


class MongoDB(AbstractDatabase):

    def __init__(self, config: BaseSettings):
        self.__client = MongoClient(config.URI, connect=False)
        self.__database = self.__client.get_database(config.DATABASE_NAME)
        self.__collection = self.__database.get_collection(config.COLLECTION_NAME)

    def __parse_query(self, query: dict):
        _query = query.copy()
        if 'id' in _query:
            _query['_id'] = _query.pop('id')

        for k, v in _query.items():
            if ObjectId.is_valid(v):
                _query[k] = ObjectId(v)
        return _query

    def __parse_result(self, result: Optional[dict]):
        if not result:
            return None

        _result = result.copy()
        if '_id' in _result:
            _result['id'] = _result.pop('_id')

        for k, v in _result.items():
            if ObjectId.is_valid(v):
                _result[k] = str(v)
        return _result

    def find_one(self, query: dict) -> dict:
        _query = self.__parse_query(query)
        result = self.__collection.find_one(filter=_query)
        return self.__parse_result(result)

    def find(self, query: dict) -> List[dict]:
        _query = self.__parse_query(query)
        result = self.__collection.find(filter=_query)
        return [self.__parse_result(item) for item in result]

    def update_one(self, query: dict, data: dict) -> dict:
        _query = self.__parse_query(query)

        self.__collection.update_one(
            filter=_query,
            update={"$set": data}
        )
        result = self.__collection.find_one(_query)
        return self.__parse_result(result)

    def create(self, data: dict) -> dict:
        result = self.__collection.insert_one(
            document=data
        )

        item = self.__collection.find_one({'_id': result.inserted_id})
        return self.__parse_result(item)

    def is_health(self) -> bool:
        return self.__client.admin.command('ping').get('ok', 0) == 1
