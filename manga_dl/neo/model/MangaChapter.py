from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from manga_dl.neo.cli.MangaFileFormat import MangaFileFormat
from manga_dl.neo.model.MangaPage import MangaPage


@dataclass
class MangaChapter:
    title: str
    number: Decimal
    volume: Optional[Decimal] = None
    published_at: datetime = datetime.utcfromtimestamp(0)
    pages: List[MangaPage] = field(default_factory=list)

    def get_filename(self, file_format: MangaFileFormat) -> str:
        filename = f"c{self.number}.{file_format.value}"
        if self.volume is not None:
            filename = f"v{self.volume}{filename}"
        return filename
