import unittest
from unittest.mock import Mock, patch
from google.oauth2 import service_account
from googleapiclient.discovery import Resource

from google_client.classes import GoogleClient


class TestGoogleClient(unittest.TestCase):

    @patch.object(service_account, 'Credentials')
    @patch.object(Resource, 'values')
    def setUp(self, mock_credentials, mock_values):
        # Mock the necessary objects
        mock_credentials.from_service_account_file.return_value = Mock()
        mock_service = Mock()
        mock_values.return_value.get.return_value = {'values': [['test_data']]}

        # Create an instance of GoogleClient with mocked objects
        self.google_client = GoogleClient()
        self.google_client.credentials = mock_credentials.from_service_account_file.return_value
        self.google_client.service = mock_service
        self.google_client.sheet = mock_service.spreadsheets.return_value

    def test_read_row(self):
        # Test the read_row method
        sheet_id = 'your_sheet_id'
        sheet_name = 'Sheet1'
        row_number = 1

        result = self.google_client.read_row(row_number, sheet_id, sheet_name)

        # Assert that the correct values were fetched
        self.assertEqual(result, [['test_data']])

    def test_write_data(self):
        # Test the write_data method
        sheet_id = 'your_sheet_id'
        sheet_name = 'Sheet1'
        row_number = 1
        column_number = 1
        data = 'new_data'

        result = self.google_client.write_data(row_number, column_number, data, sheet_id, sheet_name)

        # Assert that the write operation was successful
        self.assertTrue('updatedCells' in result)

    def test_get_cell(self):
        # Test the private method __get_cell directly (optional)
        sheet_name = 'Sheet1'
        row_number = 1
        column_number = 1

        result = self.google_client._GoogleClient__get_cell(sheet_name, row_number, column_number)

        # Assert the generated cell range is correct
        expected_range = f"{sheet_name}!A1:A1"
        self.assertEqual(result, expected_range)


if __name__ == '__main__':
    unittest.main()