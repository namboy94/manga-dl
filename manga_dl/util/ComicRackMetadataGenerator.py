from typing import Optional

from lxml import etree
from lxml.etree import Element

from manga_dl import version
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries


class ComicRackMetadataGenerator:

    def create_metadata(self, series: MangaSeries, chapter: MangaChapter, cover_file: Optional[str]) -> str:
        comic_info = etree.Element("ComicInfo")
        etree.SubElement(comic_info, "Notes").text = f"Created with manga-dl V{version}"

        self._add_basic_series_metadata(comic_info, series)
        self._add_basic_chapter_metadata(comic_info, chapter)
        self._add_pages_metadata(comic_info, chapter, cover_file)

        return etree.tostring(comic_info, pretty_print=True)

    @staticmethod
    def _add_basic_series_metadata(comic_info: Element, series: MangaSeries):
        etree.SubElement(comic_info, "Series").text = series.name

        if series.author is not None:
            etree.SubElement(comic_info, "Writer").text = series.author

        if series.artist is not None:
            etree.SubElement(comic_info, "Inker").text = series.artist
            etree.SubElement(comic_info, "Penciller").text = series.artist
            etree.SubElement(comic_info, "Colorist").text = series.artist
            etree.SubElement(comic_info, "CoverArtist").text = series.artist

    @staticmethod
    def _add_basic_chapter_metadata(comic_info: Element, chapter: MangaChapter):
        etree.SubElement(comic_info, "Title").text = chapter.title
        etree.SubElement(comic_info, "Number").text = str(chapter.number)
        etree.SubElement(comic_info, "Year").text = str(chapter.published_at.year)
        etree.SubElement(comic_info, "Month").text = str(chapter.published_at.month)
        etree.SubElement(comic_info, "Day").text = str(chapter.published_at.day)
        etree.SubElement(comic_info, "LanguageISO").text = "en"  # TODO Add this to MangaChapter
        etree.SubElement(comic_info, "ScanInformation").text = "manga-dl"  # TODO Add this to MangaChapter

        if chapter.volume is not None:
            etree.SubElement(comic_info, "Volume").text = str(chapter.volume)

    @staticmethod
    def _add_pages_metadata(comic_info: Element, chapter: MangaChapter, cover_file: Optional[str]):
        pages = etree.SubElement(comic_info, "Pages")

        if cover_file is not None:
            cover_element = etree.SubElement(pages, "Page")
            cover_element.set("Image", cover_file)
            cover_element.set("Type", "FrontCover")

        for page in chapter.pages:
            page_element = etree.SubElement(pages, "Page")
            page_element.set("Image", page.get_filename())
