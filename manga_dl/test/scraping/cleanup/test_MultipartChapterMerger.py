from typing import List, Tuple

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume
from manga_dl.scraping.cleanup.MultipartChapterMerger import MultipartChapterMerger
from manga_dl.test.testutils.TestDataFactory import TestDataFactory


class TestMultipartChapterMerger:

    def setup_method(self):
        self.under_test = MultipartChapterMerger()

    def test_merge_multipart_chapters_sequential(self):
        chapters = [
            TestDataFactory.build_chapter("A1", "1.1", 5),
            TestDataFactory.build_chapter("A2", "1.2", 10),
            TestDataFactory.build_chapter("B1", "2.1", 1),
            TestDataFactory.build_chapter("B2", "2.2", 2),
            TestDataFactory.build_chapter("B3", "2.3", 3),
            TestDataFactory.build_chapter("B4", "2.4", 4),
        ]
        series = MangaSeries("", "", volumes=[MangaVolume(chapters=chapters)])

        expected = [("A1", 15), ("B1", 10)]

        result = self.under_test.merge_multipart_chapters(series)

        assert series != result
        self._assert_title_and_pagecount(expected, result)

    def test_merge_multipart_chapters_with_gap(self):
        chapters = [
            TestDataFactory.build_chapter("A1", "1.1", 5),
            TestDataFactory.build_chapter("A2", "1.3", 10),
            TestDataFactory.build_chapter("B", "2", 15),
            TestDataFactory.build_chapter("C", "3", 20),
            TestDataFactory.build_chapter("D", "3.5", 1),
        ]
        series = MangaSeries("", "", volumes=[MangaVolume(chapters=chapters)])

        result = self.under_test.merge_multipart_chapters(series)

        assert result == series

    def test_merge_multipart_chapters_duplicates_pagecounts(self):
        chapters = [
            TestDataFactory.build_chapter("A", "1", 30),
            TestDataFactory.build_chapter("A1", "1.1", 10),
            TestDataFactory.build_chapter("A2", "1.2", 10),
            TestDataFactory.build_chapter("B", "2", 30),
            TestDataFactory.build_chapter("B1", "2.1", 10),
            TestDataFactory.build_chapter("C", "3", 10),
            TestDataFactory.build_chapter("C1", "3.1", 10),
            TestDataFactory.build_chapter("C2", "3.2", 10)
        ]
        series = MangaSeries("", "", volumes=[MangaVolume(chapters=chapters)])

        expected = [("A", 30), ("B", 30), ("C1", 20)]

        result = self.under_test.merge_multipart_chapters(series)

        assert series != result
        self._assert_title_and_pagecount(expected, result)

    def test_merge_multipart_chapters_duplicates_dates(self):
        chapters = [
            TestDataFactory.build_chapter("A", "1", 30, published_at="2020-01-01"),
            TestDataFactory.build_chapter("A1", "1.1", 15, published_at="2021-01-01"),
            TestDataFactory.build_chapter("A2", "1.2", 15, published_at="2021-01-01"),
            TestDataFactory.build_chapter("B", "2", 30, published_at="2020-01-01"),
            TestDataFactory.build_chapter("B1", "2.1", 30, published_at="2022-01-01"),
            TestDataFactory.build_chapter("C", "3", 20, published_at="2020-01-01"),
            TestDataFactory.build_chapter("C1", "3.1", 10, published_at="2019-01-01"),
            TestDataFactory.build_chapter("C2", "3.2", 10, published_at="2021-01-01")
        ]
        series = MangaSeries("", "", volumes=[MangaVolume(chapters=chapters)])

        expected = [("A1", 30), ("B1", 30), ("C1", 20)]

        result = self.under_test.merge_multipart_chapters(series)

        assert series != result
        self._assert_title_and_pagecount(expected, result)

    @staticmethod
    def _assert_title_and_pagecount(expected: List[Tuple[str, int]], result: MangaSeries):
        result_chapters = result.get_chapters()
        for i, (title, pagecount) in enumerate(expected):
            assert result_chapters[i].title == title
            assert len(result_chapters[i].pages) == pagecount
