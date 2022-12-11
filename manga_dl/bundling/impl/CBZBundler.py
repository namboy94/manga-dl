from pathlib import Path
from typing import List

from injector import inject

from manga_dl.bundling.MangaBundler import MangaBundler
from manga_dl.bundling.impl.ZipBundler import ZipBundler
from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.util.ComicRackMetadataGenerator import ComicRackMetadataGenerator
from manga_dl.util.CoverManipulator import CoverManipulator


class CBZBundler(ZipBundler, MangaBundler):

    @inject
    def __init__(self, cover_manipulator: CoverManipulator, comicrack: ComicRackMetadataGenerator):
        self.cover_manipulator = cover_manipulator
        self.comicrack = comicrack

    def get_file_format(self) -> MangaFileFormat:
        return MangaFileFormat.CBZ

    def bundle(self, images: List[DownloadedFile], destination: Path, series: MangaSeries, chapter: MangaChapter):
        cbz_file = self._add_images_to_zipfile(images, destination)

        cover_file = None
        if chapter.cover is not None:
            extension = f".{chapter.cover.filename}".split(".")[-1]
            cover_file = f"0-cover.{extension}"
            cover_data = self.cover_manipulator.add_chapter_box(chapter.cover.data, f"Ch. {chapter.number}")
            cbz_file.writestr(cover_file, cover_data)

        cbz_file.writestr("ComicInfo.xml", self.comicrack.create_metadata(series, chapter, cover_file))
        cbz_file.close()
