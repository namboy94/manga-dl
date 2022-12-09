from manga_dl.neo.model.MangaChapter import MangaChapter


class TestIdCreator:

    @staticmethod
    def create_chapter_id(chapter: MangaChapter) -> str:
        return str(hash(f"{chapter.number}+{chapter.title}"))

    @staticmethod
    def create_author_id(name: str) -> str:
        return str(hash(name))
