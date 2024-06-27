import unittest
from unittest.mock import Mock, patch

from tables.interfaces import TableInterface
from tables.classes import Table, TableFactory, TableManager


class TestTable(unittest.TestCase):
    @patch('google_client.classes.GoogleClient')
    def setUp(self, MockGoogleClient):
        self.mock_google_client = MockGoogleClient.return_value
        self.table = Table("Test Table", "sheet_id", "sheet_name", 0, 1, 2)

    def test_set_value(self):
        self.table.set_value(1, 1, "Test Value")
        self.mock_google_client.write_data.assert_called_once_with(1, 1, "Test Value", "sheet_id", "sheet_name")

    def test_get_row(self):
        self.mock_google_client.read_row.return_value = ["value1", "value2", "value3"]
        row = self.table.get_row(1)
        self.assertEqual(row, {"fsc": "value1", "phone": "value2", "status": "value3"})

    def test_table_name_property(self):
        self.assertEqual(self.table.table_name, "Test Table")


class TestTableManager(unittest.TestCase):
    def setUp(self):
        self.table_manager = TableManager()
        self.table = Mock(spec=TableInterface)
        self.table.table_name = "Test Table"

    def test_get_table(self):
        self.table_manager.new_table(self.table)
        table = self.table_manager.get_table("Test Table")
        self.assertEqual(table, self.table)

    def test_get_table_not_exist(self):
        with self.assertRaises(ValueError):
            self.table_manager.get_table("Nonexistent Table")

    def test_new_table(self):
        table = self.table_manager.new_table(self.table)
        self.assertEqual(table, self.table)
        self.assertEqual(self.table_manager.get_table("Test Table"), self.table)

    def test_new_table_already_exists(self):
        self.table_manager.new_table(self.table)
        with self.assertRaises(ValueError):
            self.table_manager.new_table(self.table)


class TestTableFactory(unittest.TestCase):
    @patch('tables.models.GoogleTables')
    @patch('tables.TableManager')
    def test_create(self, MockTableManager, MockGoogleTables):
        factory = TableFactory()
        table = factory.create("Test Table", "sheet_id", "sheet_name", 0, 1, 2)

        MockGoogleTables.assert_called_once_with("Test Table", "sheet_id", "sheet_name", 0, 1, 2)
        MockGoogleTables.return_value.save.assert_called_once()

        MockTableManager.return_value.new_table.assert_called_once()
        self.assertIsInstance(table, Table)


if __name__ == '__main__':
    unittest.main()
