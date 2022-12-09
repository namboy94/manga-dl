import shutil
import tempfile
from pathlib import Path

from manga_dl.neo.bundling.impl.DirectoryBundler import DirectoryBundler
from manga_dl.neo.model.MangaFileFormat import MangaFileFormat
from manga_dl.test.testutils.TestDataFactory import TestDataFactory


class TestDirectoryBundler:

    def setup(self):
        self.target = Path(tempfile.gettempdir()) / "dirbundler"
        self.under_test = DirectoryBundler()
        if self.target.exists():
            shutil.rmtree(self.target)

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
