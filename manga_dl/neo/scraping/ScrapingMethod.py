import importlib
import pkgutil
from abc import ABC, abstractmethod
from typing import List

from manga_dl.neo.model.MangaSeries import MangaSeries


class ScrapingMethod(ABC):

    @abstractmethod
    def is_applicable(self, series_url: str):
        pass

    @abstractmethod
    def parse_id(self, series_url: str) -> str:
        pass

    @abstractmethod
    def get_series(self, series_id: str) -> MangaSeries:
        pass


def get_scraping_methods() -> List[ScrapingMethod]:
    import manga_dl.neo.scraping.methods as methods_module
    modules = pkgutil.iter_modules(methods_module.__path__)

    for module in modules:
        importlib.import_module("manga_dl.neo.scraping.methods." + module.name)

    return list(map(lambda subclass: subclass(), ScrapingMethod.__subclasses__()))
