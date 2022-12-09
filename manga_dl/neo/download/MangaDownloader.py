import sys
from pathlib import Path
from typing import List

from injector import inject

from manga_dl.neo.bundling.MangaBundler import MangaBundler
from manga_dl.neo.model.DownloadedFile import DownloadedFile
from manga_dl.neo.model.MangaChapter import MangaChapter
from manga_dl.neo.model.MangaFileFormat import MangaFileFormat
from manga_dl.neo.model.MangaPage import MangaPage
from manga_dl.neo.model.MangaSeries import MangaSeries
from manga_dl.neo.model.MangaVolume import MangaVolume
from manga_dl.neo.util.HttpRequester import HttpRequester


class MangaDownloader:

    @inject
    def __init__(self, requester: HttpRequester, bundlers: List[MangaBundler]):
        self.requester = requester
        self.bundlers = bundlers

    def _get_bundler(self, file_format: MangaFileFormat) -> MangaBundler:
        filtered = filter(lambda x: x.is_applicable(file_format), self.bundlers)
        return next(filtered)

    def download(self, series: MangaSeries, target: Path, file_format: MangaFileFormat):
        self._prepare_target_directory(target)

        bundler = self._get_bundler(file_format)
        for volume in series.volumes:
            self._download_volume(series, volume, target, bundler)

    def _download_volume(self, series: MangaSeries, volume: MangaVolume, target: Path, bundler: MangaBundler):
        for chapter in volume.chapters:
            self._download_chapter(series, chapter, target, bundler)

    def _download_chapter(self, series: MangaSeries, chapter: MangaChapter, target: Path, bundler: MangaBundler):
        page_data = self._download_pages([page for page in chapter.pages])
        chapter_file = target / chapter.get_filename(bundler.get_file_format())

        bundler.bundle(page_data, chapter_file, series, chapter)

    def _download_pages(self, pages: List[MangaPage]) -> List[DownloadedFile]:
        return [
            DownloadedFile(
                data=self.requester.download_file(page.image_file),
                filename=page.get_filename()
            )
            for page in pages]

    def _prepare_target_directory(self, target: Path):
        if target.exists():
            do_continue = input(f"{target} already exists, delete it? (y/n)").lower() == "y"

            if not do_continue:
                print("Download aborted")
                sys.exit(0)

            if target.is_dir():
                target.rmdir()

            if target.is_file():
                target.unlink()

        target.mkdir()
