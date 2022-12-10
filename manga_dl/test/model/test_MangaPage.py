from manga_dl.model.MangaPage import MangaPage


class TestMangaPage:
    def test_get_filename(self):
        assert MangaPage("https://example.com/1.png", 15).get_filename() == "1.png"
        assert MangaPage("1.png", 15).get_filename() == "1.png"
        assert MangaPage("/home/1.png", 15).get_filename() == "1.png"
