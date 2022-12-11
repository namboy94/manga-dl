from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume
from manga_dl.scraping.cleanup.DuplicateChapterRemover import DuplicateChapterRemover
from manga_dl.test.testutils.TestDataFactory import TestDataFactory


class TestDuplicateChapterRemover:

    def setup_method(self):
        self.under_test = DuplicateChapterRemover()

    def test_remove_duplicate_chapters(self):
        chapters = [
            TestDataFactory.build_chapter("A", 1, published_at="2020-01-01"),
            TestDataFactory.build_chapter("B", 1, published_at="2021-01-01"),
            TestDataFactory.build_chapter("C", 2, published_at="2020-01-01"),
            TestDataFactory.build_chapter("D", 2.5, published_at="2021-01-01"),
            TestDataFactory.build_chapter("E", 2.5, published_at="2020-01-01"),
            TestDataFactory.build_chapter("F", 2.5, published_at="2022-01-01"),
        ]

        series = MangaSeries("", "", volumes=[MangaVolume(chapters=chapters)])
        expected = {"B", "C", "F"}

        result = self.under_test.remove_duplicate_chapters(series).volumes[0].chapters

        assert set(map(lambda x: x.title, result)) == expected
        assert result != series
