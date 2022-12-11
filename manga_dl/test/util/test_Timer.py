from unittest.mock import patch

from manga_dl.util.Timer import Timer


class TestTimer:

    def setup_method(self):
        self.under_test = Timer()

    def test_sleep(self):
        with patch("time.sleep") as sleep:
            self.under_test.sleep(10)
            sleep.assert_called_with(10)
