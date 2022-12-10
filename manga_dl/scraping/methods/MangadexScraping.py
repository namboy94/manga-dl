from typing import Optional

from injector import inject

from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.scraping.ScrapingMethod import ScrapingMethod
from manga_dl.scraping.methods.api.MangadexApi import MangadexApi


class MangadexScraping(ScrapingMethod):

    @inject
    def __init__(self, mangadex_api: MangadexApi):
        self.mangadex_api = mangadex_api

    def is_applicable(self, series_url: str):
        return "mangadex.org" in series_url

    def parse_id(self, series_url: str) -> Optional[str]:
        try:
            return series_url.split("mangadex.org/title/")[1].split("/")[0]
        except IndexError:
            return None

    def get_series(self, series_id: str, load_pages: bool = True) -> Optional[MangaSeries]:
        return self.mangadex_api.get_series(series_id, load_pages)
