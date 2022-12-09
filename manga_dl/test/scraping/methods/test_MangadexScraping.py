from unittest.mock import Mock, call

from manga_dl.neo.model.MangaSeries import MangaSeries
from manga_dl.neo.scraping.methods.MangadexScraping import MangadexScraping
from manga_dl.neo.scraping.methods.api.MangadexApi import MangadexApi


class TestMangadexScraping:

    def setup(self):
        self.manga_series = Mock(MangaSeries)
        self.mangadex_api = Mock(MangadexApi)
        self.mangadex_api.get_series.side_effect = lambda series_id: {"123": self.manga_series}.get(series_id, None)
        self.under_test = MangadexScraping(self.mangadex_api)

    def test_is_applicable(self):
        assert self.under_test.is_applicable("https://mangadex.org/title/123/abc") is True
        assert self.under_test.is_applicable("https://example.org") is False

    def test_parse_id(self):
        assert self.under_test.parse_id("https://mangadex.org/title/123/abc") == "123"
        assert self.under_test.parse_id("https://mangadex.org/title/123/") == "123"
        assert self.under_test.parse_id("https://mangadex.org/title/123") == "123"
        assert self.under_test.parse_id("https://mangadex.org") is None
        assert self.under_test.parse_id("https://example.org") is None

    def test_get_series(self):
        existing = self.under_test.get_series("123")
        not_existing = self.under_test.get_series("abc")

        assert existing == self.manga_series
        assert not_existing is None
        self.mangadex_api.get_series.assert_has_calls([call("123"), call("abc")])
