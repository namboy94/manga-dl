from decimal import Decimal
from pathlib import Path

import pytest

from manga_dl.cli.MangaDLCliOptions import MangaDLCliOptions
from manga_dl.cli.MangaDLCliParser import MangaDLCliParser
from manga_dl.model.MangaFileFormat import MangaFileFormat


class TestMangaDLCliParser:

    def setup_method(self):
        self.url = "https://example.com/123"
        self.under_test = MangaDLCliParser()

    def test_parse(self):
        args = [self.url]
        result = self.under_test.parse(args)
        expected = MangaDLCliOptions(self.url)

        assert result == expected

    def test_parse_no_url(self):
        args = []

        with pytest.raises(SystemExit) as error:
            self.under_test.parse(args)

        assert error.value.code > 0

    def test_parse_with_options(self):
        expected = MangaDLCliOptions(
            self.url,
            True,
            [Decimal("1"), Decimal("1.5")],
            Path("/tmp/mymanga.zip"),
            MangaFileFormat.ZIP,
            True,
            False
        )

        args = [self.url, "-l", "--chapters", "1", "1.5", "-o", "/tmp/mymanga.zip", "--file-format", "zip", "-v"]
        result = self.under_test.parse(args)

        assert result == expected
