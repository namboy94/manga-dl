from pathlib import Path
from typing import List

from lxml import etree

from manga_dl.neo.bundling.MangaBundler import MangaBundler
from manga_dl.neo.bundling.impl.ZipBundler import ZipBundler
from manga_dl.neo.model.DownloadedFile import DownloadedFile
from manga_dl.neo.model.MangaChapter import MangaChapter
from manga_dl.neo.model.MangaFileFormat import MangaFileFormat
from manga_dl.neo.model.MangaSeries import MangaSeries


class CBZBundler(ZipBundler, MangaBundler):

    def get_file_format(self) -> MangaFileFormat:
        return MangaFileFormat.CBZ

    def bundle(self, images: List[DownloadedFile], destination: Path, series: MangaSeries, chapter: MangaChapter):
        cbz_file = self._add_images_to_zipfile(images, destination)
        cbz_file.writestr("ComicInfo.xml", self._create_metadata_file(series, chapter))
        cbz_file.close()

    @staticmethod
    def _create_metadata_file(series: MangaSeries, chapter: MangaChapter) -> str:
        comic_info = etree.Element("ComicInfo")
        etree.SubElement(comic_info, "Title").text = chapter.title
        etree.SubElement(comic_info, "Series").text = series.name
        etree.SubElement(comic_info, "Number").text = str(chapter.number)

        if series.author is not None:
            etree.SubElement(comic_info, "Author").text = series.author

        if series.artist is not None:
            etree.SubElement(comic_info, "Artist").text = series.artist

        if chapter.volume is not None:
            etree.SubElement(comic_info, "Volume").text = str(chapter.volume)

        return etree.tostring(comic_info, pretty_print=True)
