from manga_dl.model.MangaFileFormat import MangaFileFormat


class TestMangaFileFormat:
    def test_options(self):
        enum_options = {x.value for x in MangaFileFormat}
        assert MangaFileFormat.options() == enum_options
