from unittest import TestCase
from unittest.mock import patch, MagicMock

from bson import ObjectId

from core.infrastructure.database.mongo import MongoDB


class MongoDBTest(TestCase):

    def setUp(self) -> None:
        database_mock = MagicMock()
        self.collection = database_mock.get_collection()

        database_patch = patch('pymongo.mongo_client.MongoClient.get_database', return_value=database_mock)
        database_patch.start()

        self.database = MongoDB(MagicMock(URI='localhost'))

    def test_create(self):
        data = {'My': "data"}
        result = MagicMock()
        obj = {'_id': ObjectId(), 'name': 'foo'}
        self.collection.insert_one.return_value = result
        self.collection.find_one.return_value = obj

        obj_created = self.database.create(data)

        self.collection.insert_one.assert_called_once_with(document=data)
        self.collection.find_one.assert_called_once_with({'_id': result.inserted_id})
        self.assertEqual(obj_created, {'id': str(obj['_id']), 'name': obj['name']})

    def test_find_one(self):
        expected_query = {'_id': ObjectId()}
        query = {'id': str(expected_query['_id'])}
        self.database.find_one(query)

        self.collection.find_one.assert_called_once_with(filter=expected_query)

    def test_find(self):
        expected_query = {'_id': ObjectId()}
        query = {'id': str(expected_query['_id'])}

        obj = {'_id': ObjectId(), 'name': 'foo'}
        self.collection.find.return_value = [obj] * 3

        result = self.database.find(query)

        self.collection.find.assert_called_once_with(filter=expected_query)
        self.assertEqual(result, [{'id': str(obj['_id']), 'name': obj['name']}] * 3)

    def test_update_one(self):
        data = {'My': "data"}
        expected_query = {'_id': ObjectId()}
        query = {'id': str(expected_query['_id'])}

        self.database.update_one(query, data)

        self.collection.update_one.assert_called_once_with(
            filter=expected_query,
            update={"$set": data}
        )
        self.collection.find_one.assert_called_once_with(expected_query)
