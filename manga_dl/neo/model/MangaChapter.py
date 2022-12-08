from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from manga_dl.neo.model.MangaPage import MangaPage


@dataclass
class MangaChapter:
    title: str
    number: Decimal
    pages: List[MangaPage] = field(default_factory=list)
