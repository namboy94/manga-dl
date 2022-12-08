from dataclasses import dataclass, field
from typing import List

from manga_dl.neo.model.MangaChapter import MangaChapter


@dataclass
class MangaVolume:
    volume_number: int
    chapters: List[MangaChapter] = field(default_factory=list)
