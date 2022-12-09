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

import json
import re
from typing import List

import requests

from manga_dl.entities.Chapter import Chapter
from manga_dl.scrapers.Scraper import Scraper


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
        regex = r"^https://mangadex.org/title/[a-zA-Z0-9\-]+"
        return bool(re.match(regex, url))

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
        api_base = "https://api.mangadex.org"
        mangadex_id = url.split("https://mangadex.org/title/")[1].split("/")[0]

        title_info = json.loads(requests.get(
            f"{api_base}/manga/{mangadex_id}"
        ).text)
        if title_info["result"] == "error":
            self.logger.warning(title_info["errors"])
            return []

        title = list(title_info["data"]["attributes"]["title"].values())[0]
        self.logger.debug(f"Loading chapters for {title}")

        if self.destination is None:
            destination = title
        else:
            destination = self.destination

        offset = 0
        chapters = []
        while True:
            url = f"{api_base}/chapter"
            params = {
                "translatedLanguage[]": "en",
                "manga": mangadex_id,
                "offset": offset,
                "limit": 100
            }
            response = requests.get(url, params=params)
            data = json.loads(response.text)
            result_count = len(data.get_json("data", []))
            offset += result_count

            if result_count == 0:
                break

            for result in data["data"]:

                try:
                    group = [
                        x for x in result["relationships"]
                        if x["type"] == "scanlation_group"
                    ][0]["id"]
                except IndexError:
                    group = "unknown"

                chapter_number = result["attributes"]["chapter"]
                if chapter_number is None:
                    chapter_number = "0"

                chapters.append(Chapter(
                    "https://chapter/" + result["id"],
                    "en",
                    title,
                    chapter_number,
                    destination,
                    self.format,
                    self.get_image_pages,
                    result["attributes"]["title"],
                    group,
                    {
                        "id": result["id"],
                        # "files": result["attributes"]["data"],
                        # "hash": result["attributes"]["hash"]
                    }
                ))
        self.logger.debug(f"Found {len(chapters)} chapters")
        return chapters

    @staticmethod
    def get_image_pages(_self: Chapter, _: str) -> List[str]:
        """
        Callback method for the Chapter object.
        Loads the correct image URL for a page
        :param _self: The chapter that calls this method
        :param _: The base chapter URL
        :return: The page image URLs
        """
        chapter_id = _self.extras["id"]

        at_home_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
        at_home_info = json.loads(requests.get(at_home_url).text)
        server_url = at_home_info["baseUrl"]
        chapter_hash = at_home_info["chapter"]["hash"]

        urls = [
            f"{server_url}/data/{chapter_hash}/{page}"
            for page in at_home_info["chapter"]["data"]
        ]
        return urls
