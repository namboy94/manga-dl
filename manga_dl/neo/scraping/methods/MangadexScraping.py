from manga_dl.neo.model.MangaSeries import MangaSeries
from manga_dl.neo.scraping.ScrapingMethod import ScrapingMethod


class MangadexScraping(ScrapingMethod):
    def is_applicable(self, series_url: str):
        return True

    def parse_id(self, series_url: str) -> str:
        return ""

    def get_series(self, series_id: str) -> MangaSeries:
        return MangaSeries("", [])
