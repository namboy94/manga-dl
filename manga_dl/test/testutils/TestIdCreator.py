from typing import Optional

from manga_dl.model.MangaChapter import MangaChapter


class TestIdCreator:

    @staticmethod
    def create_chapter_id(chapter: MangaChapter) -> str:
        return str(hash(f"{chapter.number}+{chapter.title}"))

    @staticmethod
    def create_author_id(name: Optional[str]) -> Optional[str]:
        return None if name is None else str(hash(name))
