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

import os
import re
import cfscrape
from typing import List
from manga_dl.entities.Chapter import Chapter
from manga_dl.scrapers.Scraper import Scraper
from bs4 import BeautifulSoup


class MangaDexScraper(Scraper):
    """
    Scraper for mangadex.org
    """

    @classmethod
    def name(cls) -> str:
        """
        :return: The name of the scraper
        """
        return "mangadex"

    @classmethod
    def url_matches(cls, url: str) -> bool:
        """
        Checks whether or not an URL matches for the scraper
        :param url: The URL to check
        :return: Whether the URL is valid
        """
        return bool(re.match(r"^https://mangadex.org/title/[0-9]+", url))

    def generate_url(self, _id: str) -> str:
        """
        Generates an URL based on an ID
        :param _id: The ID to use
        :return: The generated URL
        """
        return "https://mangadex.org/title/" + _id

    def _load_chapters(self, url: str) -> List[Chapter]:
        """
        Loads the chapters from mangadex.org
        :param url: The URL to scrape
        :return: The chapters found for the series
        """
        scraper = cfscrape.create_scraper()

        pages = []  # type: List[BeautifulSoup]

        i = 1
        limit = None

        while limit is None or i <= limit:
            page_url = os.path.join(url, "A/chapters/" + str(i))
            current_page = scraper.get(page_url)

            if current_page.status_code >= 300:
                self.logger.warning("Unsuccessful request ({})"
                                    .format(current_page.status_code))
                self.logger.debug(current_page.text)
                return []

            page_soup = BeautifulSoup(current_page.text, "html.parser")
            pages.append(page_soup)

            if limit is None:
                try:
                    limit = int(page_soup.select(".page-link")[-2].text)
                except IndexError:
                    limit = 1
                self.logger.debug("{} pages found".format(limit))

            i += 1

        series_name = pages[0].\
            select(".card-header")[0].\
            select(".mx-1")[0].text
        self.logger.debug("Series name: {}".format(series_name))

        chapters = []

        for page in pages:
            rows = page.select(".chapter-row")
            rows.pop(0)

            for row in rows:
                text = row.select(".text-truncate")[0]
                title = text.text
                url = "https://mangadex.org" + text.find("a")["href"]
                lang = row.select(".chapter-list-flag")[0].\
                    find("span")["title"].lower()

                chapter_number = title.split("Ch. ")[1].split(" -")[0]

                chapter = Chapter(
                    url,
                    lang,
                    series_name,
                    chapter_number,
                    self.destination,
                    self.format,
                    self.get_image_pages
                )
                chapters.append(chapter)
        return chapters

    @staticmethod
    def get_image_pages(url: str) -> List[str]:
        """
        Callback method for the Chapter object.
        Loads the correct image URL for a page
        :param url: The base chapter URL
        :return: The page image URLs
        """
        print(url)

        scraper = cfscrape.create_scraper()
        page = scraper.get(url)

        open("X.html", "w").write(page.text)

        exit()
