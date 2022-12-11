from pathlib import Path
from typing import List

from injector import Injector

from manga_dl.bundling.MangaBundler import MangaBundler
from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.model.MangaSeries import MangaSeries


class TestBundler(MangaBundler):

    def get_file_format(self) -> MangaFileFormat:
        return MangaFileFormat.CBZ

    def bundle(self, _: List[DownloadedFile], __: Path, ___: MangaSeries, ____: MangaChapter):  # pragma: no cover
        pass


class TestMangaBundler:

    def setup_method(self):
        self.under_test = TestBundler()

    def test_is_applicable(self):
        assert self.under_test.is_applicable(MangaFileFormat.CBZ) is True
        assert self.under_test.is_applicable(MangaFileFormat.DIR) is False
        assert self.under_test.is_applicable(MangaFileFormat.ZIP) is False

    def test_get_bundlers(self):
        injector = Injector()
        bundlers = self.under_test.get_bundlers(injector)
        assert len(bundlers) == len(MangaFileFormat) + 1  # because of test bundler
