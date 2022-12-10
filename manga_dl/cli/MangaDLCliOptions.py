from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import List

from manga_dl.model.MangaFileFormat import MangaFileFormat


@dataclass
class MangaDLCliOptions:
    url: str
    list_chapters: bool = False
    chapters: List[Decimal] = field(default_factory=list)
    out: Path = Path.home() / "Downloads/Manga"
    file_format: MangaFileFormat = MangaFileFormat.CBZ
    verbose: bool = False
    quiet: bool = False
