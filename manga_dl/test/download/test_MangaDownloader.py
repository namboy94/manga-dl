import itertools
import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, call

from manga_dl.bundling.MangaBundler import MangaBundler
from manga_dl.download.MangaDownloader import MangaDownloader
from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.test.testutils.TestDataFactory import TestDataFactory
from manga_dl.util.HttpRequester import HttpRequester


class TestMangaDownloader:

    def setup_method(self):
        self.dummy_bytes = bytes("Hello World", "utf8")
        self.file_type = MangaFileFormat.CBZ
        self.testing_path = Path(tempfile.gettempdir()) / "testing_download"
        self.requester = Mock(HttpRequester)
        self.requester.download_file.return_value = self.dummy_bytes
        self.bundler = Mock(MangaBundler)
        self.bundler.is_applicable.return_value = True
        self.bundler.get_file_format.return_value = self.file_type
        self.under_test = MangaDownloader(self.requester, [self.bundler])

        if self.testing_path.exists():
            shutil.rmtree(self.testing_path)

    def test_download(self):
        series = TestDataFactory.build_series()
        chapters = series.get_chapters()
        pages = list(itertools.chain(*[chapter.pages for chapter in chapters]))
        last_chapter = series.get_chapters()[-1]
        last_chapter_dest = self.testing_path / series.name / last_chapter.get_filename(self.file_type)
        last_chapter_image_files = [
            DownloadedFile(self.dummy_bytes, page.get_filename())
            for page in last_chapter.pages
        ]

        self.under_test.download(series, self.testing_path, self.file_type)

        self.requester.download_file.assert_has_calls([call(page.image_file) for page in pages])
        self.bundler.bundle.assert_called_with(last_chapter_image_files, last_chapter_dest, series, last_chapter)
        assert (self.testing_path / series.name).is_dir()

    def test_download_single_chapter(self):
        series = TestDataFactory.build_series()
        last_chapter = series.get_chapters()[-1]
        last_chapter_image_files = [
            DownloadedFile(self.dummy_bytes, page.get_filename())
            for page in last_chapter.pages
        ]

        self.under_test.download_single_chapter(series, last_chapter, self.testing_path, self.file_type)

        self.requester.download_file.assert_has_calls([call(page.image_file) for page in last_chapter.pages])
        self.bundler.bundle.assert_called_with(last_chapter_image_files, self.testing_path, series, last_chapter)
