import importlib
import pkgutil
from abc import ABC, abstractmethod
from typing import List, Optional

from injector import Injector

from manga_dl.neo.model.MangaSeries import MangaSeries


class ScrapingMethod(ABC):

    @abstractmethod  # pragma: no cover
    def is_applicable(self, series_url: str):
        pass

    @abstractmethod  # pragma: no cover
    def parse_id(self, series_url: str) -> Optional[str]:
        pass

    @abstractmethod  # pragma: no cover
    def get_series(self, series_id: str) -> Optional[MangaSeries]:
        pass

    @staticmethod
    def get_scraping_methods(injector: Injector) -> List["ScrapingMethod"]:
        import manga_dl.neo.scraping.methods as methods_module
        modules = pkgutil.iter_modules(methods_module.__path__)

        for module in modules:
            importlib.import_module("manga_dl.neo.scraping.methods." + module.name)

        return list(map(lambda subclass: injector.get(subclass), ScrapingMethod.__subclasses__()))  # type: ignore
