from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple

from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaFileFormat import MangaFileFormat
from manga_dl.model.MangaPage import MangaPage


@dataclass
class MangaChapter:
    title: str
    number: Decimal
    volume: Optional[Decimal] = None
    published_at: datetime = datetime.utcfromtimestamp(0)
    pages: List[MangaPage] = field(default_factory=list)
    cover: Optional[DownloadedFile] = None

    def get_filename(self, file_format: MangaFileFormat) -> str:
        filename = f"c{self.number}-{self.title}"

        if self.volume is not None:
            filename = f"v{self.volume}{filename}"

        if file_format != MangaFileFormat.DIR:
            filename = f"{filename}.{file_format.value}"

        return filename

    def get_macro_micro_chapter(self) -> Tuple[int, int]:
        after_decimal_point_decimal = self.number % 1
        after_decimal_point = int("0" + str(after_decimal_point_decimal).replace(".", ""))
        return int(self.number - after_decimal_point_decimal), int(after_decimal_point)

    def is_special_chapter(self) -> bool:
        macro, micro = self.get_macro_micro_chapter()
        return macro == 0 or micro != 0
