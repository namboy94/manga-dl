import logging
from pathlib import Path
from typing import List

from injector import inject

from manga_dl.bundling.MangaBundler import MangaBundler
from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.model.MangaPage import MangaPage
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume
from manga_dl.util.HttpRequester import HttpRequester


class MangaDownloader:
    logger = logging.getLogger("MangaDownloader")

    @inject
    def __init__(self, requester: HttpRequester, bundlers: List[MangaBundler]):
        self.requester = requester
        self.bundlers = bundlers

    def _get_bundler(self, file_format: MangaFileFormat) -> MangaBundler:
        filtered = filter(lambda x: x.is_applicable(file_format), self.bundlers)
        return next(filtered)

    def download(self, series: MangaSeries, target: Path, file_format: MangaFileFormat):
        series_dir = target / series.name
        series_dir.mkdir(parents=True, exist_ok=True)
        bundler = self._get_bundler(file_format)
        for volume in series.volumes:
            self._download_volume(series, volume, series_dir, bundler)

    def download_single_chapter(
            self, series: MangaSeries, chapter: MangaChapter, target: Path, file_format: MangaFileFormat
    ):
        bundler = self._get_bundler(file_format)
        self._download_chapter(series, chapter, target, bundler)

    def _download_volume(self, series: MangaSeries, volume: MangaVolume, target: Path, bundler: MangaBundler):
        for chapter in volume.chapters:
            chapter_file = target / chapter.get_filename(bundler.get_file_format())
            self._download_chapter(series, chapter, chapter_file, bundler)

    def _download_chapter(self, series: MangaSeries, chapter: MangaChapter, target: Path, bundler: MangaBundler):
        self.logger.info(f"Downloading chapter {chapter.number}")
        page_data = self._download_pages([page for page in chapter.pages])
        bundler.bundle(page_data, target, series, chapter)

    def _download_pages(self, pages: List[MangaPage]) -> List[DownloadedFile]:

        downloaded = []
        for page in pages:
            page_data = self.requester.download_file(page.image_file)
            page_data = b"Missing" if page_data is None else page_data
            downloaded.append(DownloadedFile(page_data, page.get_filename()))

        return downloaded
