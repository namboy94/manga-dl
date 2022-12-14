from decimal import Decimal
from typing import List, Union

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
        expected = [1, 2, 3]

        result = self.under_test.normalize_chapters(series)

        self._assert_chapter_order(expected, result)
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
        expected = [1.5, 2]

        result = self.under_test.normalize_chapters(series)

        self._assert_chapter_order(expected, result)
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
        expected = [1, 2]

        result = self.under_test.normalize_chapters(series)

        self._assert_chapter_order(expected, result)
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
        expected = [1, 2, 3, 4, 5, 6, 10]

        result = self.under_test.normalize_chapters(series)

        self._assert_chapter_order(expected, result)
        assert result != series

    def test_tonikawa(self):
        series = MangaSeries("30f3ac69-21b6-45ad-a110-d011b7aaadaa", "Tonikaku Kawaii", volumes=[
            MangaVolume(volume_number=Decimal(14), chapters=[
                TestDataFactory.build_chapter("A", 136, volume=14),
                TestDataFactory.build_chapter("A", 136.5, volume=14),
            ]),
            MangaVolume(volume_number=Decimal(15), chapters=[
                TestDataFactory.build_chapter("A", 140.5, volume=15),
                TestDataFactory.build_chapter("A", 141, volume=15),
                TestDataFactory.build_chapter("A", 142, volume=15),
                TestDataFactory.build_chapter("A", 143, volume=15),
                TestDataFactory.build_chapter("A", 144, volume=15),
                TestDataFactory.build_chapter("A", 145, volume=15),
                TestDataFactory.build_chapter("A", 146, volume=15),
                TestDataFactory.build_chapter("A", 147, volume=15),
                TestDataFactory.build_chapter("A", 147.5, volume=15),
            ]),
            MangaVolume(volume_number=Decimal(16), chapters=[
                TestDataFactory.build_chapter("B1", 1, volume=16),
                TestDataFactory.build_chapter("B2", 2, volume=16),
                TestDataFactory.build_chapter("B2", 3, volume=16),
                TestDataFactory.build_chapter("B2", 4, volume=16),
                TestDataFactory.build_chapter("C1", 137, volume=16),
                TestDataFactory.build_chapter("C2", 138, volume=16),
                TestDataFactory.build_chapter("C2", 139, volume=16),
                TestDataFactory.build_chapter("C2", 140, volume=16),
                TestDataFactory.build_chapter("C2", 148, volume=16),
                TestDataFactory.build_chapter("C2", 148.5, volume=16),
            ]),
            MangaVolume(volume_number=Decimal(17), chapters=[
                TestDataFactory.build_chapter("E", 149, volume=17),
            ])
        ])
        expected = [
            136, 136.5,
            140.5, 141, 142, 143, 144, 145, 146, 147, 147.5,
            140.51, 140.52, 140.53, 140.54, 137, 138, 139, 140, 148, 148.5,
            149
        ]

        result = self.under_test.normalize_chapters(series)

        self._assert_chapter_order(expected, result)
        assert result != series

    @staticmethod
    def _assert_chapter_order(expected_order: List[Union[str, int, float]], result: MangaSeries):
        expected = list(map(lambda x: str(x), expected_order))
        result_numbers = list(map(lambda x: str(x.number), result.get_chapters()))
        assert expected == result_numbers
