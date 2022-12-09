from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from manga_dl.neo.model.MangaFileFormat import MangaFileFormat
from manga_dl.neo.model.MangaPage import MangaPage


@dataclass
class MangaChapter:
    title: str
    number: Decimal
    volume: Optional[Decimal] = None
    published_at: datetime = datetime.utcfromtimestamp(0)
    pages: List[MangaPage] = field(default_factory=list)

    def get_filename(self, file_format: MangaFileFormat) -> str:
        filename = f"c{self.number}-{self.title}"

        if self.volume is not None:
            filename = f"v{self.volume}{filename}"

        if file_format != MangaFileFormat.DIR:
            filename = f"{filename}.{file_format.value}"

        return filename
