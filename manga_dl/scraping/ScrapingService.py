from typing import List, Optional

from injector import inject

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.scraping.ScrapingMethod import ScrapingMethod


class ScrapingService:

    @inject
    def __init__(self, scraping_methods: List[ScrapingMethod]):
        self.scraping_methods = scraping_methods

    def scrape(self, series_url: str, load_pages: bool = True) -> Optional[MangaSeries]:
        scraping_method = self._find_applicable_scraping_method(series_url)

        if scraping_method is None:
            return None

        series_id = scraping_method.parse_id(series_url)

        if series_id is None:
            return None

        return scraping_method.get_series(series_id, load_pages)

    def _find_applicable_scraping_method(self, series_url: str) -> Optional[ScrapingMethod]:
        filtered = filter(lambda x: x.is_applicable(series_url), self.scraping_methods)
        return next(filtered, None)
