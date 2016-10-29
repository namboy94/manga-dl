"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from typing import List
from toktokkie.modules.objects.manga.MangaVolume import MangaVolume


class GenericMangaScraper(object):
    """
    Class that handles scraping of Manga series from http://jb2448.info/ (Pokemon Special Gallery)
    """

    @staticmethod
    def url_match(manga_url: str) -> bool:
        """
        Checks if a URL matches the pattern expected by the scraper

        :param manga_url: the URL to check
        :return: True if it matches, False otherwise
        """
        return manga_url.startswith("http://jb2448.info")

    @staticmethod
    def scrape_volumes_from_url(manga_url: str, manga_directory: str, skip_existing_chapters: bool = False,
                                max_threads: int = 1, verbose: bool = False) -> List[MangaVolume]:
        """
        Scrapes a given URL

        :param manga_url: the given URL to scrape
        :param manga_directory: the manga directory, which can be used to skip existing chapters
        :param skip_existing_chapters: Flag that can be set to skip existing chapters, thereby increasing scraping speed
        :param max_threads: the maximum numbers of threads to use
        :param verbose: Sets the verbosity flag. Defaults to no output
        :return: a list of volumes, which should also contain chapters
        """
        raise NotImplementedError()
