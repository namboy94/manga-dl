from manga_dl.model.DownloadedFile import DownloadedFile


class TestDownloadedFile:
    def test_get_extension(self):
        assert DownloadedFile(bytes("A", "utf8"), "file.png").get_extension() == "png"
        assert DownloadedFile(bytes("A", "utf8"), "my.file.jpg").get_extension() == "jpg"
        assert DownloadedFile(bytes("A", "utf8"), "myfile").get_extension() == ""
