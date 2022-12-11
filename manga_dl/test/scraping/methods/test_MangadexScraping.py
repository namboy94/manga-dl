from unittest.mock import Mock, call

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.scraping.methods.MangadexScraping import MangadexScraping
from manga_dl.scraping.methods.api.MangadexApi import MangadexApi


class TestMangadexScraping:

    def setup_method(self):
        self.manga_series = Mock(MangaSeries)
        self.manga_series_no_pages = Mock(MangaSeries)
        self.mangadex_api = Mock(MangadexApi)

        options = {"123": {True: self.manga_series, False: self.manga_series_no_pages}}
        self.mangadex_api.get_series.side_effect = \
            lambda series_id, load_pages: options.get(series_id, {}).get(load_pages, None)
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
        no_pages = self.under_test.get_series("123", False)

        assert existing == self.manga_series
        assert not_existing is None
        assert no_pages == self.manga_series_no_pages
        self.mangadex_api.get_series.assert_has_calls([call("123", True), call("abc", True), call("123", False)])
