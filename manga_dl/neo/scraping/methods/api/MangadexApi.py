import itertools
import logging
from decimal import Decimal
from typing import Optional, Dict, Any, List, Tuple

from injector import inject

from manga_dl.neo.model.MangaChapter import MangaChapter
from manga_dl.neo.model.MangaPage import MangaPage
from manga_dl.neo.model.MangaSeries import MangaSeries
from manga_dl.neo.model.MangaVolume import MangaVolume
from manga_dl.neo.util.DateConverter import DateConverter
from manga_dl.neo.util.HttpRequester import HttpRequester
from manga_dl.neo.util.Timer import Timer


class MangadexApi:
    base_url = "https://api.mangadex.org"
    logger = logging.getLogger("MangadexApi")

    @inject
    def __init__(self, http_requester: HttpRequester, date_converter: DateConverter, timer: Timer):
        self.timer = timer
        self.http_requester = http_requester
        self.date_converter = date_converter

    def get_series(self, series_id: str) -> Optional[MangaSeries]:
        self.logger.info(f"Loading data for series {series_id}")
        try:
            title, author, artist = self._load_series_info(series_id)
            self.logger.info(f"Found info: title={title}, author={author}, artist={artist}")
            volumes = self._load_volumes(series_id)
            return MangaSeries(series_id, title, author, artist, volumes)
        except ValueError:
            return None

    def _call_api(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.timer.sleep(0.5)
        response = self.http_requester.get_json(f"{self.base_url}/{endpoint}", params)

        if response is None or response["result"] == "error":
            self.logger.warning(response)
            raise ValueError("Error while using the mangadex API")

        return response

    def _call_api_ignore_errors(self, endpoint: str) -> Optional[Dict[str, Any]]:
        try:
            return self._call_api(endpoint)
        except ValueError:
            return None

    def _load_volumes(self, series_id: str) -> List[MangaVolume]:
        chapters = self._load_chapters(series_id)
        grouped_by_volume = itertools.groupby(chapters, lambda chapter: chapter.volume)
        return [
            MangaVolume(volume_number=volume_number, chapters=list(chapters))
            for volume_number, chapters in grouped_by_volume
        ]

    def _load_chapters(self, mangadex_id: str) -> List[MangaChapter]:
        chapters = []

        offset = 0
        end_reached = False
        while not end_reached:
            params = self._build_chapter_page_params(mangadex_id, offset)
            self.logger.info(f"Loading chapters {offset}-{offset + params['limit']}")

            chapters_data = self._call_api("chapter", params).get("data", [])
            chapter_count = len(chapters_data)

            chapters += self._parse_chapters(chapters_data)

            offset += chapter_count
            end_reached = chapter_count == 0

        return chapters

    @staticmethod
    def _build_chapter_page_params(mangadex_id: str, offset: int) -> Dict[str, Any]:
        return {
            "translatedLanguage[]": "en",
            "manga": mangadex_id,
            "offset": offset,
            "limit": 100
        }

    def _parse_chapters(self, chapters_data: List[Dict[str, Any]]) -> List[MangaChapter]:
        all_chapters = [
            self._parse_chapter(chapter_data)
            for chapter_data in chapters_data
        ]
        return [x for x in all_chapters if x is not None]

    def _parse_chapter(self, chapter_data: Dict[str, Any]) -> Optional[MangaChapter]:
        attributes = chapter_data["attributes"]
        is_external = attributes["externalUrl"] is not None

        if is_external:
            return None

        raw_chapter_number = attributes["chapter"]
        raw_volume_number = attributes["volume"]

        title = attributes["title"] if attributes["title"] != "" else f"Chapter {raw_chapter_number}"
        chapter_number = Decimal("0" if raw_chapter_number is None else raw_chapter_number)
        volume_number = None if raw_volume_number is None else Decimal(raw_volume_number)
        created_at = self.date_converter.convert_to_datetime(attributes["createdAt"])
        pages = self._load_pages(chapter_data["id"])

        self.logger.info(f"Parsed chapter {raw_chapter_number}")

        return MangaChapter(
            title=title,
            number=chapter_number,
            volume=volume_number,
            published_at=created_at,
            pages=pages
        )

    def _load_pages(self, chapter_id: str) -> List[MangaPage]:
        at_home_endpoint = f"at-home/server/{chapter_id}"
        at_home_info = self._call_api_ignore_errors(at_home_endpoint)

        if at_home_info is None:
            return []

        server_url = at_home_info["baseUrl"]
        chapter_hash = at_home_info["chapter"]["hash"]

        urls = [
            MangaPage(image_file=f"{server_url}/data/{chapter_hash}/{page}", page_number=i + 1)
            for i, page in enumerate(at_home_info["chapter"]["data"])
        ]
        return urls

    def _load_series_info(self, series_id: str) -> Tuple[str, Optional[str], Optional[str]]:
        title_info = self._call_api(f"manga/{series_id}")
        title = list(title_info["data"]["attributes"]["title"].values())[0]
        relations = title_info["data"]["relationships"]
        author = self._load_author_name(self.get_first_id_with_type_from_relations(relations, "author"))
        artist = self._load_author_name(self.get_first_id_with_type_from_relations(relations, "artist"))

        return title, author, artist

    def _load_author_name(self, author_id: str) -> Optional[str]:
        author_info = self._call_api(f"author/{author_id}")
        return author_info["data"]["attributes"]["name"]

    @staticmethod
    def get_first_id_with_type_from_relations(relations: List[Dict[str, str]], key: str) -> Optional[str]:
        return next(filter(lambda x: x["type"] == key, relations), {"id": None})["id"]
