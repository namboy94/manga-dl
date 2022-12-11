from manga_dl.cli.MangaDLCli import MangaDLCli
from manga_dl.util.MangaDLDependencyInjector import MangaDLDependencyInjector


class TestMangaDLDependencyInjector:
    def test_get(self):
        cli = MangaDLDependencyInjector.get(MangaDLCli)
        assert isinstance(cli, MangaDLCli)
