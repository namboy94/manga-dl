from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from manga_dl.neo.model.MangaChapter import MangaChapter


@dataclass
class MangaVolume:
    volume_number: Optional[Decimal] = None
    chapters: List[MangaChapter] = field(default_factory=list)
