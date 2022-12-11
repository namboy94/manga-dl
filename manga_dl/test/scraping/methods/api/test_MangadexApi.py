from unittest.mock import Mock

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.scraping.methods.api.MangadexApi import MangadexApi
from manga_dl.test.scraping.methods.api.MockedMangadexHttpRequester import MockedMangadexHttpRequester
from manga_dl.test.testutils.TestDataFactory import TestDataFactory
from manga_dl.test.testutils.TestIdCreator import TestIdCreator
from manga_dl.util.DateConverter import DateConverter
from manga_dl.util.Timer import Timer


class TestMangadexApi:

    def setup_method(self):
        self.dateconverter = DateConverter()
        self.timer = Mock(Timer)
        self.requester = MockedMangadexHttpRequester(self.timer)
        self.under_test = MangadexApi(self.requester, self.dateconverter, self.timer)

        self.series = TestDataFactory.build_series()
        self.requester.add_series(self.series)

    def test_get_series(self):
        result = self.under_test.get_series(self.series.id)

        assert result == self.series

    def test_get_series_no_pages(self):
        result = self.under_test.get_series(self.series.id, False)

        for chapter in result.get_chapters():
            assert chapter.pages == []

    def test_get_series_only_external_links(self):
        self.requester.set_external_chapters(True)

        result = self.under_test.get_series(self.series.id).get_chapters()

        assert result == []

    def test_get_series_http_error(self):
        self.requester.set_errors(False, True)

        result = self.under_test.get_series(self.series.id)

        assert result is None

    def test_get_series_api_error(self):
        self.requester.set_errors(True, False)

        result = self.under_test.get_series(self.series.id)

        assert result is None

    def test_get_series_no_pages_info_found(self):
        chapter_id = TestIdCreator.create_chapter_id(self.series.volumes[0].chapters[0])
        self.requester.add_endpoint_override(f"at-home/server/{chapter_id}", None)

        result = self.under_test.get_series(self.series.id)

        assert result.volumes[0].chapters[0].pages == []

    def test_get_series_no_author_info_found(self):
        series = MangaSeries(id="100", name="100", author=None, artist=None)
        self.requester.add_series(series)

        result = self.under_test.get_series(series.id)

        assert result.author is None
        assert result.artist is None

    def test_get_series_use_default_cover(self):
        series = MangaSeries(id="100", name="100", volumes=[
            TestDataFactory.build_minimal_volume("1", cover=None),
            TestDataFactory.build_minimal_volume(None, cover="Default"),
        ])
        self.requester.add_series(series)

        result = self.under_test.get_series(series.id)

        assert result.volumes[0].cover == result.volumes[1].cover
        assert result.volumes[0].cover.filename == "Default.png"

    def test_get_series_use_minimal_cover(self):
        series = MangaSeries(id="1000", name="100", volumes=[
            TestDataFactory.build_minimal_volume("1", cover="one"),
            TestDataFactory.build_minimal_volume("2", cover="two"),
            TestDataFactory.build_minimal_volume("3", cover=None),
        ])
        self.requester.add_series(series)

        result = self.under_test.get_series(series.id)

        assert result.volumes[2].cover == result.volumes[0].cover
        assert result.volumes[2].cover.filename == "one.png"
