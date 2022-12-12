from manga_dl.test.testutils.TestDataFactory import TestDataFactory
from manga_dl.util.StringFormatter import StringFormatter


class TestStringFormatter:

    def setup_method(self):
        self.under_test = StringFormatter()

    def test_format_series(self):
        series = TestDataFactory.build_series()
        series.volumes[0].chapters.append(TestDataFactory.build_chapter("", 10))
        result = self.under_test.format_series(series)

        expected = "[123]TestManga (author=TestAuthor, artist=TestArtist)\n" \
                   "  Vol. 1\n" \
                   "    Ch. 1 - A\n" \
                   "    Ch. 2 - B\n" \
                   "    Ch. 10 - Untitled\n" \
                   "  No Volume\n" \
                   "    Ch. 1.5 - S"

        assert result == expected
