import logging
import sys

from injector import inject

from manga_dl.cli.MangaDLCliOptions import MangaDLCliOptions
from manga_dl.cli.MangaDLCliParser import MangaDLCliParser
from manga_dl.download.MangaDownloader import MangaDownloader
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.scraping.ScrapingService import ScrapingService
from manga_dl.util.StringFormatter import StringFormatter


class MangaDLCli:

    @inject
    def __init__(
            self,
            parser: MangaDLCliParser,
            scraper: ScrapingService,
            downloader: MangaDownloader,
            formatter: StringFormatter
    ):
        self._parser = parser
        self._scraper = scraper
        self._downloader = downloader
        self._formatter = formatter
        self._options = MangaDLCliOptions("")

    def run(self):
        self._options = self._parser.parse(sys.argv[1:])
        self._adjust_log_level()
        series = self._scraper.scrape(self._options.url, not self._options.list_chapters)
        self._list_chapters(series)
        self._download_chapters(series)

    def _adjust_log_level(self):
        if self._options.verbose:
            logging.basicConfig(level=logging.INFO)
        if self._options.quiet:
            logging.disable(logging.CRITICAL)

    def _list_chapters(self, series: MangaSeries):
        if not self._options.list_chapters:
            return
        print(self._formatter.format_series(series))

    def _download_chapters(self, series: MangaSeries):
        if self._options.list_chapters:
            return
        self._downloader.download(series, self._options.out, self._options.file_format)
