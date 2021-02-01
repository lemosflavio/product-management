from unittest import TestCase
from unittest.mock import MagicMock, call

from core.infrastructure.repository import ProductRepository


class ProductRepositoryTest(TestCase):

    def setUp(self) -> None:
        self.database = MagicMock()
        self.profile = MagicMock()
        self.repo = ProductRepository(self.database, self.profile)

    def test_find_one(self):
        query = {'id': 1}
        item = MagicMock()
        self.database.find_one.return_value = item

        self.repo.find_one(query)

        self.database.find_one.assert_called_once_with(query=query)
        self.profile.map_to_entity.assert_called_once_with(item)

    def test_find(self):
        query = {'id': 1}
        item = MagicMock()
        self.database.find.return_value = [item] * 3

        self.repo.find(query)

        self.database.find.assert_called_once_with(query=query)
        self.profile.map_to_entity.assert_has_calls([call(item)] * 3)

    def test_update_one(self):
        entity = MagicMock()
        data = MagicMock()
        item = MagicMock()
        query = {'id': entity.id_}

        self.database.update_one.return_value = item
        self.profile.map_to_data.return_value = data

        self.repo.update_one(entity)

        self.database.update_one.assert_called_once_with(query=query, data=data)
        self.profile.map_to_entity.assert_called_once_with(item)
        self.profile.map_to_data.assert_called_once_with(entity)

    def test_create(self):
        entity = MagicMock()
        data = MagicMock()
        item = MagicMock()

        self.database.create.return_value = item
        self.profile.map_to_data.return_value = data

        self.repo.create(entity)

        self.database.create.assert_called_once_with(data)
        self.profile.map_to_entity.assert_called_once_with(item)
        self.profile.map_to_data.assert_called_once_with(entity)

    def test_map_to_entity_return_none_if_item_has_no_value(self):
        self.assertIsNone(self.repo.map_to_entity(None))
        self.assertEqual(self.repo.map_to_entity({}), {})
