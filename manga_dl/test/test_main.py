from unittest.mock import patch, Mock

from manga_dl.cli.MangaDLCli import MangaDLCli
from manga_dl.main import main


class TestMain:

    @patch("manga_dl.main.MangaDLDependencyInjector.get")
    def test_main(self, inject_get_mock: Mock):
        cli_mock = Mock(MangaDLCli)
        inject_get_mock.return_value = cli_mock

        main()

        inject_get_mock.assert_called_with(MangaDLCli)
        cli_mock.run.assert_called_once()
