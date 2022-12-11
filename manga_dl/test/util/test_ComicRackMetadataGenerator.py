from decimal import Decimal
from typing import Optional, Union, List

from lxml import etree
from lxml.etree import fromstring

from manga_dl.test.testutils.TestDataFactory import TestDataFactory
from manga_dl.util.ComicRackMetadataGenerator import ComicRackMetadataGenerator


class TestComicRackMetadataGenerator:

    def setup_method(self):
        self.series = TestDataFactory.build_series()
        self.chapter = self.series.get_chapters()[0]
        self.cover_file: Optional[str] = "image.png"
        self.under_test = ComicRackMetadataGenerator()

    def test_create_metadata(self):
        metadata = fromstring(self.under_test.create_metadata(self.series, self.chapter, self.cover_file))
        self._assert_metadata(metadata)

    def test_create_metadata_no_author_or_artist(self):
        self.series.artist = None
        self.series.author = None

        metadata = fromstring(self.under_test.create_metadata(self.series, self.chapter, self.cover_file))
        self._assert_metadata(metadata)
        self._assert_tags_missing(metadata, ["Writer", "Inker", "Penciller", "Colorist", "CoverArtist"])

    def test_create_metadata_no_volume(self):
        self.chapter.volume = None

        metadata = fromstring(self.under_test.create_metadata(self.series, self.chapter, self.cover_file))
        self._assert_metadata(metadata)
        self._assert_tags_missing(metadata, ["Volume"])

    def test_create_metadata_no_cover(self):
        self.cover_file = None

        metadata = fromstring(self.under_test.create_metadata(self.series, self.chapter, self.cover_file))
        self._assert_metadata(metadata)

    def _assert_metadata(self, metadata: etree):
        self._assert_series_metadata(metadata)
        self._assert_chapter_metadata(metadata)
        self._assert_pages_metadata(metadata)

    def _assert_series_metadata(self, metadata: etree):
        self._assert_tag(metadata, "Series", self.series.name)
        self._assert_tag(metadata, "Writer", self.series.author)
        self._assert_tag(metadata, "Inker", self.series.artist)
        self._assert_tag(metadata, "Penciller", self.series.artist)
        self._assert_tag(metadata, "Colorist", self.series.artist)
        self._assert_tag(metadata, "CoverArtist", self.series.artist)

    def _assert_chapter_metadata(self, metadata: etree):
        self._assert_tag(metadata, "Title", self.chapter.title)
        self._assert_tag(metadata, "Number", self.chapter.number)
        self._assert_tag(metadata, "Year", self.chapter.published_at.year)
        self._assert_tag(metadata, "Month", self.chapter.published_at.month)
        self._assert_tag(metadata, "Day", self.chapter.published_at.day)
        self._assert_tag(metadata, "LanguageISO", "en")
        self._assert_tag(metadata, "ScanInformation", "manga-dl")
        self._assert_tag(metadata, "Volume", self.chapter.volume)

    def _assert_pages_metadata(self, metadata: etree):
        assert metadata.find("Pages") is not None
        pages = metadata.find("Pages").findall("Page")

        if self.cover_file is not None:
            cover = pages.pop(0)
            assert cover.get("Image") == self.cover_file
            assert cover.get("Type") == "FrontCover"

        assert len(self.chapter.pages) == len(pages)

        for page in self.chapter.pages:
            assert pages.pop(0).get("Image") == page.get_filename()

    @staticmethod
    def _assert_tag(metadata: etree, tag: str, expected: Optional[Union[str, int, Decimal]]):
        if expected is None:
            assert metadata.find(tag) is None
        else:
            assert metadata.find(tag).text == str(expected)

    def _assert_tags_missing(self, metadata: etree, tags: List[str]):
        for tag in tags:
            self._assert_tag(metadata, tag, None)
