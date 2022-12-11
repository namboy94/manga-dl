from decimal import Decimal

from pytest_unordered import unordered

from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume


class TestMangaSeries:
    def test_get_chapters(self):
        chapters = [
            MangaChapter(title="s", number=Decimal(1.5)),
            MangaChapter(title="x", number=Decimal(1), volume=Decimal(1)),
            MangaChapter(title="y", number=Decimal(2), volume=Decimal(2)),
            MangaChapter(title="z", number=Decimal(3), volume=Decimal(2)),
        ]
        series = MangaSeries(id="1", name="a", author="b", artist="c", volumes=[
            MangaVolume(volume_number=Decimal(1), chapters=[chapters[0]]),
            MangaVolume(volume_number=Decimal(2), chapters=chapters[2:]),
            MangaVolume(volume_number=None, chapters=[chapters[1]]),
        ])

        assert series.get_chapters() == unordered(chapters)
