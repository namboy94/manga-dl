import argparse
from decimal import Decimal
from pathlib import Path
from typing import List

from manga_dl.cli.MangaDLCliOptions import MangaDLCliOptions
from manga_dl.model.MangaFileFormat import MangaFileFormat


class MangaDLCliParser:

    def __init__(self):
        defaults = MangaDLCliOptions("")
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument("url",
                                  help="The URL from which to download the manga")
        self._parser.add_argument("-c", "--chapters", nargs="+", default=defaults.chapters,
                                  help="Specifies which chapters to download")
        self._parser.add_argument("-l", "--list-chapters", action="store_true",
                                  help="Lists all found chapters")
        self._parser.add_argument("-f", "--file-format",
                                  choices=MangaFileFormat.options(), default=defaults.file_format.value,
                                  help="The format in which to store the chapters")
        self._parser.add_argument("-o", "--out", default=defaults.out,
                                  help="Specifies the output path")
        self._parser.add_argument("-v", "--verbose", action="store_true",
                                  help="Enable more verbose output")
        self._parser.add_argument("-q", "--quiet", action="store_true",
                                  help="Disable all output")

    def parse(self, cli_args: List[str]) -> MangaDLCliOptions:
        args = self._parser.parse_args(cli_args)
        args.chapters = list(map(lambda chapter: Decimal(chapter), args.chapters))
        args.file_format = MangaFileFormat(args.file_format)
        args.out = Path(args.out)
        return MangaDLCliOptions(**vars(args))
