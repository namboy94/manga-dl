import itertools
from dataclasses import dataclass, field
from typing import List, Optional

from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaVolume import MangaVolume


@dataclass
class MangaSeries:
    id: str
    name: str
    author: Optional[str] = None
    artist: Optional[str] = None
    volumes: List[MangaVolume] = field(default_factory=list)

    def get_chapters(self) -> List[MangaChapter]:
        return list(itertools.chain(*[volume.chapters for volume in self.volumes]))
