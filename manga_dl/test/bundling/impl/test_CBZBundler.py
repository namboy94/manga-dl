import tempfile
from pathlib import Path
from xml.etree.ElementTree import fromstring
from zipfile import ZipFile

from pytest_unordered import unordered

from manga_dl.bundling.impl.CBZBundler import CBZBundler
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.test.testutils.TestDataFactory import TestDataFactory


class TestCBZBundler:

    def setup(self):
        self.target = Path(tempfile.gettempdir()) / "cbzbundler.cbz"
        self.under_test = CBZBundler()
        if self.target.exists():
            self.target.unlink()

    def test_is_applicable(self):
        assert self.under_test.is_applicable(MangaFileFormat.CBZ) is True
        assert self.under_test.is_applicable(MangaFileFormat.ZIP) is False

    def test_get_file_format(self):
        assert self.under_test.get_file_format() == MangaFileFormat.CBZ

    def test_bundle(self):
        series = TestDataFactory.build_series()
        chapter = series.get_chapters()[0]
        files = TestDataFactory.build_downloaded_files(chapter)

        self.under_test.bundle(files, self.target, series, chapter)

        assert self.target.is_file()
        with ZipFile(self.target) as cbzfile:
            expected_files = unordered([image.filename for image in files] + ["ComicInfo.xml", "0-cover.png"])
            assert cbzfile.namelist() == expected_files

            xml = fromstring(cbzfile.read("ComicInfo.xml"))
            assert xml.find("Series").text == series.name
            assert xml.find("Writer").text == series.author
            assert xml.find("Inker").text == series.artist
            assert xml.find("Title").text == chapter.title
            assert xml.find("Number").text == str(chapter.number)
            assert xml.find("Volume").text == str(chapter.volume)

    def test_bundle_no_volume(self):
        series = TestDataFactory.build_series()
        chapter = series.get_chapters()[0]
        files = TestDataFactory.build_downloaded_files(chapter)
        chapter.volume = None

        self.under_test.bundle(files, self.target, series, chapter)

        with ZipFile(self.target) as cbzfile:
            xml = fromstring(cbzfile.read("ComicInfo.xml"))
            assert xml.find("Volume") is None

    def test_bundle_no_author_or_artist(self):
        series = TestDataFactory.build_series()
        chapter = series.get_chapters()[0]
        files = TestDataFactory.build_downloaded_files(chapter)
        series.artist = None
        series.author = None

        self.under_test.bundle(files, self.target, series, chapter)

        with ZipFile(self.target) as cbzfile:
            xml = fromstring(cbzfile.read("ComicInfo.xml"))
            assert xml.find("Artist") is None
            assert xml.find("Author") is None
