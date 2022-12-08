from dataclasses import dataclass, field
from typing import List

from manga_dl.neo.model.MangaVolume import MangaVolume


@dataclass
class MangaSeries:
    author: str
    volumes: List[MangaVolume] = field(default_factory=list)
