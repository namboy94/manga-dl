from decimal import Decimal
from typing import Optional, List

from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaPage import MangaPage
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.model.MangaVolume import MangaVolume
from manga_dl.test.testutils.TestIdCreator import TestIdCreator


class TestDataFactory:

    @staticmethod
    def build_series() -> MangaSeries:
        coverfile = DownloadedFile(b"CoverImage", "cover.png")
        volumes = [
            MangaVolume(volume_number=Decimal(1),
                        chapters=[TestDataFactory.build_chapter("A", 1, 5, 1),
                                  TestDataFactory.build_chapter("B", 2, 3, 1)],
                        cover=coverfile),
            MangaVolume(chapters=[TestDataFactory.build_chapter("S", 1.5, 10)], cover=coverfile)
        ]
        return MangaSeries(id="123", name="TestManga", author="TestAuthor", artist="TestArtist", volumes=volumes)

    @staticmethod
    def build_chapter(title: str, number: float, page_count: int, volume: Optional[float] = None) -> MangaChapter:
        decimal_volume = None if volume is None else Decimal(volume)
        dummy_chapter = MangaChapter(title=title, number=Decimal(number), volume=decimal_volume)
        chapter_id = TestIdCreator.create_chapter_id(dummy_chapter)
        pages = [
            MangaPage(image_file=f"example.com/data/{chapter_id}/{i}.png", page_number=i + 1)
            for i in range(0, page_count)
        ]
        return MangaChapter(
            title=title,
            number=dummy_chapter.number,
            volume=dummy_chapter.volume,
            pages=pages,
            cover=DownloadedFile(b"CoverImage", "cover.png")
        )

    @staticmethod
    def build_downloaded_files(chapter: MangaChapter) -> List[DownloadedFile]:
        return [DownloadedFile(bytes(page.image_file, "utf8"), page.get_filename()) for page in chapter.pages]
