import importlib
import pkgutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from injector import Injector

from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.model.MangaSeries import MangaSeries


class MangaBundler(ABC):

    def is_applicable(self, file_format: MangaFileFormat) -> bool:
        return self.get_file_format() == file_format

    @abstractmethod  # pragma: no cover
    def get_file_format(self) -> MangaFileFormat:
        pass

    @abstractmethod  # pragma: no cover
    def bundle(self, images: List[DownloadedFile], destination: Path, series: MangaSeries, chapter: MangaChapter):
        pass

    @staticmethod
    def get_bundlers(injector: Injector) -> List["MangaBundler"]:
        import manga_dl.bundling.impl as impl_module
        modules = pkgutil.iter_modules(impl_module.__path__)

        for module in modules:
            importlib.import_module("manga_dl.bundling.impl." + module.name)

        return list(map(lambda subclass: injector.get(subclass), MangaBundler.__subclasses__()))  # type: ignore
