import logging
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from manga_dl.cli.MangaDLCli import MangaDLCli
from manga_dl.cli.MangaDLCliOptions import MangaDLCliOptions
from manga_dl.cli.MangaDLCliParser import MangaDLCliParser
from manga_dl.download.MangaDownloader import MangaDownloader
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.scraping.ScrapingService import ScrapingService


class TestMangaDLCli:

    def setup_method(self):
        self.url = "example.org"
        self.target = Path(tempfile.gettempdir())
        self.series = Mock(MangaSeries)
        self.options = MangaDLCliOptions(self.url, out=self.target)

        self.parser = Mock(MangaDLCliParser)
        self.parser.parse.return_value = self.options
        self.scraper = Mock(ScrapingService)
        self.scraper.scrape.return_value = self.series
        self.downloader = Mock(MangaDownloader)

        self.under_test = MangaDLCli(self.parser, self.scraper, self.downloader)

    def test_run_download(self):
        self.under_test.run()

        self.scraper.scrape.assert_called_with(self.url)
        self.downloader.download.assert_called_with(self.series, self.target, self.options.file_format)

    def test_run_list(self):
        self.options.list_chapters = True
        self.under_test.run()

        self.scraper.scrape.assert_called_with(self.url)
        self.downloader.download.assert_not_called()

    def test_verbose(self):
        self.options.verbose = True

        with patch("logging.basicConfig") as basicConfig:
            self.under_test.run()
            basicConfig.assert_called_with(level=logging.INFO)

    def test_quiet(self):
        self.options.quiet = True

        with patch("logging.disable") as disable:
            self.under_test.run()
            disable.assert_called_with(logging.CRITICAL)
