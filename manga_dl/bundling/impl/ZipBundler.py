from pathlib import Path
from typing import List
from zipfile import ZipFile

from manga_dl.bundling.MangaBundler import MangaBundler
from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.model.MangaSeries import MangaSeries


class ZipBundler(MangaBundler):

    def get_file_format(self) -> MangaFileFormat:
        return MangaFileFormat.ZIP

    def bundle(self, images: List[DownloadedFile], destination: Path, series: MangaSeries, chapter: MangaChapter):
        zip_file = self._add_images_to_zipfile(images, destination)
        zip_file.close()

    @staticmethod
    def _add_images_to_zipfile(images: List[DownloadedFile], destination: Path) -> ZipFile:
        zip_file = ZipFile(destination, "w")
        for image in images:
            zip_file.writestr(image.filename, image.data)
        return zip_file
