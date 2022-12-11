from unittest.mock import Mock

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.scraping.ScrapingMethod import ScrapingMethod
from manga_dl.scraping.ScrapingService import ScrapingService
from manga_dl.scraping.cleanup.DuplicateChapterRemover import DuplicateChapterRemover
from manga_dl.scraping.cleanup.MultipartChapterMerger import MultipartChapterMerger


class TestScrapingService:

    def setup_method(self):
        self.url = "https://example.com/123"
        self.id = "123"

        self.series = Mock(MangaSeries)
        self.series_no_pages = Mock(MangaSeries)
        self.scraping_method = Mock(ScrapingMethod)
        self.scraping_method.is_applicable.side_effect = lambda series_url: "example.com" in series_url
        self.scraping_method.parse_id.side_effect = lambda series_url: series_url.rsplit("/", 1)[1]
        self.scraping_method.get_series.side_effect = \
            lambda series_id, load_pages: self.series if load_pages else self.series_no_pages

        self.dupe_remover = Mock(DuplicateChapterRemover)
        self.chapter_merger = Mock(MultipartChapterMerger)
        self.dupe_remover.remove_duplicate_chapters.side_effect = lambda x: x
        self.chapter_merger.merge_multipart_chapters.side_effect = lambda x: x

        self.under_test = ScrapingService(self.dupe_remover, self.chapter_merger, [self.scraping_method])

    def test_scrape(self):
        result = self.under_test.scrape(self.url)

        self.scraping_method.is_applicable.assert_called_with(self.url)
        self.scraping_method.parse_id.assert_called_with(self.url)
        self.scraping_method.get_series.assert_called_with(self.id, True)
        self.dupe_remover.remove_duplicate_chapters.assert_called_with(self.series)
        self.chapter_merger.merge_multipart_chapters.assert_called_with(self.series)

        assert result == self.series

    def test_scrape_no_page_loading(self):
        result = self.under_test.scrape(self.url, False)

        self.scraping_method.is_applicable.assert_called_with(self.url)
        self.scraping_method.parse_id.assert_called_with(self.url)
        self.scraping_method.get_series.assert_called_with(self.id, False)
        self.dupe_remover.remove_duplicate_chapters.assert_called_with(self.series_no_pages)
        self.chapter_merger.merge_multipart_chapters.assert_called_with(self.series_no_pages)

        assert result == self.series_no_pages

    def test_scrape_invalid_url(self):
        invalid_url = "https://notvalid.com"
        result = self.under_test.scrape(invalid_url)

        self.scraping_method.is_applicable.assert_called_with(invalid_url)
        self.scraping_method.parse_id.assert_not_called()
        self.scraping_method.get_series.assert_not_called()
        self.dupe_remover.remove_duplicate_chapters.assert_not_called()
        self.chapter_merger.merge_multipart_chapters.assert_not_called()

        assert result is None

    def test_scrape_invalid_id(self):
        self.scraping_method.parse_id.side_effect = lambda x: None

        result = self.under_test.scrape(self.url)

        assert result is None

    def test_scrape_scrape_result_is_none(self):
        self.scraping_method.get_series.side_effect = lambda x, y: None

        result = self.under_test.scrape(self.url)

        assert result is None

    def test_scrape_cleanup_correct(self):
        first = Mock(MangaSeries)
        second = Mock(MangaSeries)
        self.dupe_remover.remove_duplicate_chapters.side_effect = lambda _: first
        self.chapter_merger.merge_multipart_chapters.side_effect = lambda _: second

        result = self.under_test.scrape(self.url)

        self.dupe_remover.remove_duplicate_chapters.assert_called_with(self.series)
        self.chapter_merger.merge_multipart_chapters.assert_called_with(first)
        assert result == second
