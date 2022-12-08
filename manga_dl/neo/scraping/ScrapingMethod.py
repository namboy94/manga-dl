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
    def get_volumes(self, series_id: str) -> List[MangaSeries]:
        pass
