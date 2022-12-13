from decimal import Decimal

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume
from manga_dl.scraping.cleanup.ChapterNormalizer import ChapterNormalizer
from manga_dl.test.testutils.TestDataFactory import TestDataFactory


class TestChapterNormalizer:

    def setup_method(self):
        self.under_test = ChapterNormalizer()

    def test_normalize_chapters_chapter_based_on_volume(self):
        series = MangaSeries("", "", volumes=[
            MangaVolume(volume_number=Decimal(1), chapters=[
                TestDataFactory.build_chapter("A", 1, volume=1),
            ]),
            MangaVolume(volume_number=Decimal(2), chapters=[
                TestDataFactory.build_chapter("B", 1, volume=2),
            ]),
            MangaVolume(volume_number=Decimal(3), chapters=[
                TestDataFactory.build_chapter("C", 1, volume=3),
            ]),
        ])

        result = self.under_test.normalize_chapters(series)

        assert result.get_chapters()[1].number == Decimal(2)
        assert result.get_chapters()[2].number == Decimal(3)
        assert result != series

    def test_normalize_chapters_no_volumes(self):
        series = MangaSeries("", "")

        result = self.under_test.normalize_chapters(series)

        assert result == series

    def test_normalize_chapters_no_chapters_in_previous_volume(self):
        series = MangaSeries("", "", volumes=[
            MangaVolume(volume_number=Decimal(1)),
            MangaVolume(volume_number=Decimal(2), chapters=[
                TestDataFactory.build_chapter("B", 1, volume=2),
            ]),
        ])

        result = self.under_test.normalize_chapters(series)

        assert result == series

    def test_normalize_chapters_decimal_chapter_in_previous_volume(self):
        series = MangaSeries("", "", volumes=[
            MangaVolume(volume_number=Decimal(1), chapters=[
                TestDataFactory.build_chapter("B", "1.5", volume=2),
            ]),
            MangaVolume(volume_number=Decimal(2), chapters=[
                TestDataFactory.build_chapter("B", 1, volume=2),
            ]),
        ])

        result = self.under_test.normalize_chapters(series)

        assert result.get_chapters()[1].number == Decimal(2)
        assert result != series

    def test_normalize_chapters_unknown_volume(self):
        series = MangaSeries("", "", volumes=[
            MangaVolume(volume_number=Decimal(1), chapters=[
                TestDataFactory.build_chapter("A", 1, volume=1)
            ]),
            MangaVolume(volume_number=None, chapters=[
                TestDataFactory.build_chapter("B", 1)
            ]),
        ])

        result = self.under_test.normalize_chapters(series)

        assert result.get_chapters()[1].number == Decimal(2)
        assert result.get_chapters()[1].title == "B"
        assert result != series

    def test_normalize_chapters_mixed(self):
        series = MangaSeries("", "", volumes=[
            MangaVolume(volume_number=Decimal(1), chapters=[
                TestDataFactory.build_chapter("A", 1, volume=1),
                TestDataFactory.build_chapter("B", 2, volume=1)
            ]),
            MangaVolume(volume_number=Decimal(2), chapters=[
                TestDataFactory.build_chapter("C", 3, volume=2)
            ]),
            MangaVolume(volume_number=Decimal(3), chapters=[
                TestDataFactory.build_chapter("D", 1, volume=3),
                TestDataFactory.build_chapter("E", 2, volume=3),
                TestDataFactory.build_chapter("F", 4, volume=3),
                TestDataFactory.build_chapter("F", 10, volume=3),
            ])
        ])

        result = self.under_test.normalize_chapters(series)

        assert result.get_chapters()[2].number == Decimal(3)
        assert result.get_chapters()[3].number == Decimal(4)
        assert result.get_chapters()[4].number == Decimal(5)
        assert result.get_chapters()[5].number == Decimal(6)
        assert result.get_chapters()[6].number == Decimal(10)
        assert result != series
