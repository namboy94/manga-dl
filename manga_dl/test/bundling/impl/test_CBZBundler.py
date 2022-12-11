import tempfile
from pathlib import Path
from unittest.mock import Mock

from manga_dl.bundling.impl.CBZBundler import CBZBundler
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.test.testutils.TestDataFactory import TestDataFactory
from manga_dl.util.ComicRackMetadataGenerator import ComicRackMetadataGenerator
from manga_dl.util.CoverManipulator import CoverManipulator


class TestCBZBundler:

    def setup_method(self):
        self.target = Path(tempfile.gettempdir()) / "cbzbundler.cbz"
        self.comicrack = Mock(ComicRackMetadataGenerator)
        self.cover_manipulator = Mock(CoverManipulator)

        self.comicrack.create_metadata.return_value = "ComicRack XML"
        self.cover_manipulator.add_chapter_box.side_effect = lambda in_bytes, _: in_bytes

        self.under_test = CBZBundler(self.cover_manipulator, self.comicrack)
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

        self.comicrack.create_metadata.assert_called_once()
        self.cover_manipulator.add_chapter_box.assert_called_once()
