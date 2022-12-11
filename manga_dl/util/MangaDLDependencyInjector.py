from typing import List, TypeVar, Type

from injector import Injector

from manga_dl.bundling.MangaBundler import MangaBundler
from manga_dl.scraping.ScrapingMethod import ScrapingMethod

T = TypeVar("T")


class MangaDLDependencyInjector:

    @staticmethod
    def get(cls: Type[T]) -> T:
        injector = Injector()
        injector.binder.multibind(List[ScrapingMethod], ScrapingMethod.get_scraping_methods(injector))
        injector.binder.multibind(List[MangaBundler], MangaBundler.get_bundlers(injector))
        return injector.get(cls)
