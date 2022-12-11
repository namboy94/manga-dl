import shutil
import tempfile
from pathlib import Path

from manga_dl.bundling.impl.DirectoryBundler import DirectoryBundler
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.test.testutils.TestDataFactory import TestDataFactory


class TestDirectoryBundler:

    def setup_method(self):
        self.target = Path(tempfile.gettempdir()) / "dirbundler"
        self.under_test = DirectoryBundler()
        if self.target.exists():
            shutil.rmtree(self.target)

    def test_is_applicable(self):
        assert self.under_test.is_applicable(MangaFileFormat.DIR) is True

    def test_get_file_format(self):
        assert self.under_test.get_file_format() == MangaFileFormat.DIR

    def test_bundle(self):
        series = TestDataFactory.build_series()
        chapter = series.get_chapters()[0]
        files = TestDataFactory.build_downloaded_files(chapter)

        self.under_test.bundle(files, self.target, series, chapter)

        assert self.target.is_dir()
        for image_file in files:
            assert (self.target / image_file.filename).is_file()
