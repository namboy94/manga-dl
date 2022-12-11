from typing import List, Optional

from injector import inject

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.scraping.ScrapingMethod import ScrapingMethod
from manga_dl.scraping.cleanup.DuplicateChapterRemover import DuplicateChapterRemover
from manga_dl.scraping.cleanup.MultipartChapterMerger import MultipartChapterMerger


class ScrapingService:

    @inject
    def __init__(
            self,
            duplicate_chapter_remover: DuplicateChapterRemover,
            multipart_chapter_merger: MultipartChapterMerger,
            scraping_methods: List[ScrapingMethod]
    ):
        self.duplicate_chapter_remover = duplicate_chapter_remover
        self.multipart_chapter_merger = multipart_chapter_merger
        self.scraping_methods = scraping_methods

    def scrape(self, series_url: str, load_pages: bool = True) -> Optional[MangaSeries]:
        scraping_method = self._find_applicable_scraping_method(series_url)

        if scraping_method is None:
            return None

        series_id = scraping_method.parse_id(series_url)

        if series_id is None:
            return None

        series = scraping_method.get_series(series_id, load_pages)
        series = self.duplicate_chapter_remover.remove_duplicate_chapters(series)
        series = self.multipart_chapter_merger.merge_multipart_chapters(series)
        return series

    def _find_applicable_scraping_method(self, series_url: str) -> Optional[ScrapingMethod]:
        filtered = filter(lambda x: x.is_applicable(series_url), self.scraping_methods)
        return next(filtered, None)
