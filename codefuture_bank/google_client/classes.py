import string

from google.oauth2 import service_account
from googleapiclient.discovery import build

from google_client.interfaces import GoogleClientInterface
from google_client.serializer import SerializerInterface, Serializer

CREDENTIALS_FILE = 'codefuturetelegramsbank-token.json'


class GoogleClient(GoogleClientInterface):

    def init(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def read_row(self, row: int, sheet_id, sheet_name, *args, **kwargs) -> SerializerInterface:
        range_name = f'{sheet_name}!{row}:{row}'
        result = self.sheet.values().get(spreadsheetId=sheet_id,
                                         range=range_name).execute()
        return Serializer(result.get('values', [])).row

    def write_data(self, row, column, data, sheet_id, sheet_name, *args, **kwargs):
        range_name = self.__get_cell(sheet_name, row, column)
        values = [[data]]
        body = {'values': values}
        result = self.sheet.values().update(spreadsheetId=sheet_id,
                                            range=range_name,
                                            valueInputOption="RAW",
                                            body=body).execute()
        return result

    def __get_cell(self, sheet_name, row, column):
        cell = f"{string.ascii_letters[column]}{row}"
        return f"{sheet_name}!{cell}:{cell}"


GOOGLE_CLIENT = GoogleClient()
GoogleClient()
