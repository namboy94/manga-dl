from datetime import datetime

from manga_dl.util.DateConverter import DateConverter


class TestDateConverter:

    def setup_method(self):
        self.under_test = DateConverter()
        self.datetime = datetime(year=2020, month=1, day=2, hour=10, minute=5, second=15)
        self.date_string = "2020-01-02T10:05:15"

    def test_convert_to_string(self):
        assert self.under_test.convert_to_string(self.datetime) == self.date_string

    def test_convert_to_datetime(self):
        assert self.under_test.convert_to_datetime(self.date_string) == self.datetime
        assert self.under_test.convert_to_datetime(self.date_string + "+00:00") == self.datetime
        assert self.under_test.convert_to_datetime(self.under_test.convert_to_string(self.datetime)) == self.datetime
