"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

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
LICENSE"""

import logging
from typing import Optional, List, Set
from manga_dl.entities.Chapter import Chapter


class Scraper:
    """
    Specifies the Capabilities of a manga download site scraper
    """

    def __init__(
            self,
            _format: str = "cbz",
            destination: Optional[str] = None,
            languages: Optional[Set[str]] = None
    ):
        """
        Initializes the Scraper object
        :param _format: The format in which to store chapters
        :param destination: The destination directory in
                            which to store chapters
        :param languages: Set of languages for which to check
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.format = _format
        self.destination = destination
        if languages is None:
            self.languages = {"english", "gb", "us"}
        else:
            self.languages = languages

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the scraper
        """
        raise NotImplementedError()

    @classmethod
    def url_matches(cls, url: str) -> bool:
        """
        Checks whether or not an URL matches for the scraper
        :param url: The URL to check
        :return: Whether the URL is valid
        """
        raise NotImplementedError()

    def generate_url(self, _id: str) -> str:
        """
        Generates an URL based on an ID
        :param _id: The ID to use
        :return: The generated URL
        """
        raise NotImplementedError()

    def load_chapters(
            self,
            url: Optional[str] = None,
            _id: Optional[str] = None
    ) -> List[Chapter]:
        """
        Loads a list of Chapter objects for an URL or ID
        Only one of either an URL or an ID is required
        :param url: The URL
        :param _id: The ID
        :return: The list of chapters
        """
        if url is None and _id is None:
            self.logger.warning("Neither URL or ID provided. Can't continue.")
            return []
        elif url is not None and not self.url_matches(url):
            self.logger.warning("Invalid URL. Can't continue.")
            return []
        elif _id is not None:
            url = self.generate_url(_id)

        chapters = self._load_chapters(str(url))

        # Both sort steps are necessary!
        chapters.sort(
            key=lambda x: str(x.chapter_number).zfill(15)
        )
        chapters.sort(
            key=lambda x: str(x.chapter_number.split(".")[0]).zfill(15)
        )
        return list(filter(lambda x: x.language in self.languages, chapters))

    def _load_chapters(self, url: str) -> List[Chapter]:
        """
        Scraper-specific implementation that loads chapters from the website
        :param url: The URL to scrape
        :return: The list of chapters found while scraping
        """
        raise NotImplementedError()
