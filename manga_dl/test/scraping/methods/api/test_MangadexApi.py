from unittest.mock import Mock

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume
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
        self.under_test = MangadexApi(self.requester, self.dateconverter)

        self.series = TestDataFactory.build_series()
        self.requester.add_series(self.series)

    def test_get_series(self):
        result = self.under_test.get_series(self.series.id)

        assert result == self.series

    def test_get_series_titles_unavailable(self):
        self.series.get_chapters()[0].title = None
        self.series.get_chapters()[1].title = ""

        result = self.under_test.get_series(self.series.id)

        assert result != self.series
        assert result.get_chapters()[0].title == "Chapter 1"
        assert result.get_chapters()[1].title == "Chapter 2"

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

    def test_get_series_volumes_correctly_grouped(self):
        series = TestDataFactory.build_series("AAA")
        separated_chapter = TestDataFactory.build_chapter(
            title="ABC", number=str(series.volumes[0].chapters[-1].number + 1), volume=series.volumes[0].volume_number
        )
        series.volumes.append(MangaVolume(series.volumes[0].volume_number, [separated_chapter]))
        self.requester.add_series(series)

        result = self.under_test.get_series(series.id)

        assert len(result.volumes) == len(series.volumes) - 1
        assert result.volumes[0].chapters[-1] == separated_chapter
