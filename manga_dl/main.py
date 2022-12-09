"""
Copyright 2015-2017 Hermann Krumrey

This file is part of manga-dl.

manga-dl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

manga-dl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with manga-dl.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import List

from injector import Injector

from manga_dl.neo.cli.MangaDLCli import MangaDLCli
from manga_dl.neo.scraping.ScrapingMethod import ScrapingMethod, get_scraping_methods


def main():
    injector = Injector()
    injector.binder.multibind(List[ScrapingMethod], get_scraping_methods(injector))
    cli = injector.get(MangaDLCli)
    cli.run()


if __name__ == "__main__":
    main()
