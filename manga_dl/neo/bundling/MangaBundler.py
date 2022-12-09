from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from manga_dl.neo.cli.MangaFileFormat import MangaFileFormat
from manga_dl.neo.download.DownloadedFile import DownloadedFile
from manga_dl.neo.model.MangaChapter import MangaChapter
from manga_dl.neo.model.MangaSeries import MangaSeries


class MangaBundler(ABC):

    @abstractmethod
    def is_applicable(self, file_format: MangaFileFormat) -> bool:
        pass

    @abstractmethod
    def get_file_format(self) -> MangaFileFormat:
        pass

    @abstractmethod
    def bundle(self, images: List[DownloadedFile], destination: Path, series: MangaSeries, chapter: MangaChapter):
        pass
