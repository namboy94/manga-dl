from unittest.mock import Mock

from manga_dl.neo.model.MangaSeries import MangaSeries
from manga_dl.neo.scraping.ScrapingMethod import ScrapingMethod
from manga_dl.neo.scraping.ScrapingService import ScrapingService


class TestScrapingService:

    def setup(self):
        self.url = "https://example.com/123"
        self.id = "123"

        self.series = Mock(MangaSeries)
        self.scraping_method = Mock(ScrapingMethod)
        self.scraping_method.is_applicable.side_effect = lambda series_url: "example.com" in series_url
        self.scraping_method.parse_id.side_effect = lambda series_url: series_url.rsplit("/", 1)[1]
        self.scraping_method.get_volumes.side_effect = lambda series_id: [self.series]
        self.underTest = ScrapingService([self.scraping_method])

    def test_scrape(self):
        result = self.underTest.scrape(self.url)

        self.scraping_method.is_applicable.assert_called_with(self.url)
        self.scraping_method.parse_id.assert_called_with(self.url)
        self.scraping_method.get_volumes.assert_called_with(self.id)

        assert result == [self.series]

    def test_scrape_invalid_url(self):
        invalid_url = "https://notvalid.com"
        result = self.underTest.scrape(invalid_url)

        self.scraping_method.is_applicable.assert_called_with(invalid_url)
        self.scraping_method.parse_id.assert_not_called()
        self.scraping_method.get_volumes.assert_not_called()

        assert result == []
