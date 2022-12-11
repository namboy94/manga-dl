import tempfile
from pathlib import Path
from zipfile import ZipFile

from pytest_unordered import unordered

from manga_dl.bundling.impl.ZipBundler import ZipBundler
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.test.testutils.TestDataFactory import TestDataFactory


class TestZipBundler:

    def setup_method(self):
        self.target = Path(tempfile.gettempdir()) / "zipbundler.zip"
        self.under_test = ZipBundler()
        if self.target.exists():
            self.target.unlink()

    def test_is_applicable(self):
        assert self.under_test.is_applicable(MangaFileFormat.ZIP) is True

    def test_get_file_format(self):
        assert self.under_test.get_file_format() == MangaFileFormat.ZIP

    def test_bundle(self):
        series = TestDataFactory.build_series()
        chapter = series.get_chapters()[0]
        files = TestDataFactory.build_downloaded_files(chapter)

        self.under_test.bundle(files, self.target, series, chapter)

        assert self.target.is_file()
        with ZipFile(self.target) as zipfile:
            assert zipfile.namelist() == unordered([image.filename for image in files])
