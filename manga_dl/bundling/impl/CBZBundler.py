from pathlib import Path
from typing import List

from lxml import etree

from manga_dl.bundling.MangaBundler import MangaBundler
from manga_dl.bundling.impl.ZipBundler import ZipBundler
from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.model.MangaSeries import MangaSeries


class CBZBundler(ZipBundler, MangaBundler):

    def get_file_format(self) -> MangaFileFormat:
        return MangaFileFormat.CBZ

    def bundle(self, images: List[DownloadedFile], destination: Path, series: MangaSeries, chapter: MangaChapter):
        cbz_file = self._add_images_to_zipfile(images, destination)

        cover_file = None
        if chapter.cover is not None:
            extension = f".{chapter.cover.filename}".split(".")[-1]
            cover_file = f"0-cover.{extension}"
            cbz_file.writestr(cover_file, chapter.cover.data)

        cbz_file.writestr("ComicInfo.xml", self._create_metadata_file(series, chapter, cover_file))
        cbz_file.close()

    @staticmethod
    def _create_metadata_file(series: MangaSeries, chapter: MangaChapter, cover_file: str) -> str:
        comic_info = etree.Element("ComicInfo")
        pages = etree.SubElement(comic_info, "Pages")

        etree.SubElement(comic_info, "Title").text = chapter.title
        etree.SubElement(comic_info, "Series").text = series.name
        etree.SubElement(comic_info, "Number").text = str(chapter.number)

        if series.author is not None:
            etree.SubElement(comic_info, "Writer").text = series.author

        if series.artist is not None:
            etree.SubElement(comic_info, "Inker").text = series.artist

        if chapter.volume is not None:
            etree.SubElement(comic_info, "Volume").text = str(chapter.volume)

        if cover_file is not None:
            cover_element = etree.SubElement(pages, "Page")
            cover_element.set("image", cover_file)

        return etree.tostring(comic_info, pretty_print=True)
