from manga_dl.model.MangaPage import MangaPage


class TestMangaPage:
    def test_get_filename(self):
        assert MangaPage("https://example.com/1.png", 1).get_filename() == "0001-1.png"
        assert MangaPage("2.png", 15).get_filename() == "0015-2.png"
        assert MangaPage("/home/3.png", 2345).get_filename() == "2345-3.png"
