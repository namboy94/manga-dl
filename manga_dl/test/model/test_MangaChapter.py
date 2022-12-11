from decimal import Decimal

from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaFileFormat import MangaFileFormat


class TestMangaChapter:
    def test_get_filename(self):
        assert MangaChapter("A", Decimal(1)).get_filename(MangaFileFormat.ZIP) == "c1-A.zip"
        assert MangaChapter("B", Decimal(2), Decimal(1)).get_filename(MangaFileFormat.CBZ) == "v1c2-B.cbz"
        assert MangaChapter("C", Decimal(2.5)).get_filename(MangaFileFormat.DIR) == "c2.5-C"

    def test_get_macro_micro_chapter(self):
        assert MangaChapter("A", Decimal("12")).get_macro_micro_chapter() == (12, 0)
        assert MangaChapter("B", Decimal("1.5")).get_macro_micro_chapter() == (1, 5)
        assert MangaChapter("C", Decimal("30.15")).get_macro_micro_chapter() == (30, 15)
        assert MangaChapter("D", Decimal("0.2")).get_macro_micro_chapter() == (0, 2)

    def test_is_special_chapter(self):
        assert MangaChapter("A", Decimal("12")).is_special_chapter() is False
        assert MangaChapter("B", Decimal("1.5")).is_special_chapter() is True
        assert MangaChapter("C", Decimal("30.1")).is_special_chapter() is True
        assert MangaChapter("D", Decimal("0.2")).is_special_chapter() is True
        assert MangaChapter("E", Decimal("0")).is_special_chapter() is True
