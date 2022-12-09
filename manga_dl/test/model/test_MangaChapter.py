from decimal import Decimal

from manga_dl.neo.model.MangaChapter import MangaChapter
from manga_dl.neo.model.MangaFileFormat import MangaFileFormat


class TestMangaChapter:
    def test_get_filename(self):
        assert MangaChapter("A", Decimal(1)).get_filename(MangaFileFormat.ZIP) == "c1-A.zip"
        assert MangaChapter("B", Decimal(2), Decimal(1)).get_filename(MangaFileFormat.CBZ) == "v1c2-B.cbz"
        assert MangaChapter("C", Decimal(2.5)).get_filename(MangaFileFormat.DIR) == "c2.5-C"
