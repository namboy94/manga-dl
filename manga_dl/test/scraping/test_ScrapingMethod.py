from injector import Injector

from manga_dl.scraping.ScrapingMethod import ScrapingMethod


class TestScrapingMethod:
    def test_get_scraping_methods(self):
        injector = Injector()
        methods = ScrapingMethod.get_scraping_methods(injector)
        assert len(methods) >= 1
