import itertools
from typing import Optional, Dict, Any, Union, List

from manga_dl.model.DownloadedFile import DownloadedFile
from manga_dl.model.MangaChapter import MangaChapter
from manga_dl.model.MangaSeries import MangaSeries
from manga_dl.test.testutils.TestIdCreator import TestIdCreator
from manga_dl.util.HttpRequester import HttpRequester
from manga_dl.util.Timer import Timer


class MockedMangadexHttpRequester(HttpRequester):

    def __init__(self, timer: Timer):
        super().__init__(timer)
        self._series: List[MangaSeries] = []
        self._external_chapters = False
        self._create_http_error = False
        self._create_api_error = False
        self._endpoint_overrides: Dict[str, Any] = {}
        self._file_cache: Dict[str, DownloadedFile] = {}

    def add_series(self, series: MangaSeries):
        self._series.append(series)

    def set_external_chapters(self, external_chapters: bool):
        self._external_chapters = external_chapters

    def set_errors(self, http: bool, api: bool):
        self._create_http_error = http
        self._create_api_error = api

    def add_endpoint_override(self, endpoint: str, response: Optional[Dict[str, Any]]):
        self._endpoint_overrides[endpoint] = response

    def get_json(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:

        params = {} if params is None else params

        if self._create_http_error:
            return None

        if self._create_api_error:
            return {"result": "error"}

        endpoint = url.replace("https://api.mangadex.org/", "")

        if endpoint in self._endpoint_overrides:
            return self._endpoint_overrides[endpoint]

        if endpoint == "chapter":
            return self._build_response(self._get_chapter_data(params))

        else:
            static_responses: Dict[str, Any] = {}
            for series in self._series:
                static_responses |= self._create_manga_endpoint_responses(series)
                static_responses |= self._create_author_endpoint_responses(series.author)
                static_responses |= self._create_author_endpoint_responses(series.artist)
                static_responses |= self._create_chapter_page_endpoint_responses(series)
                static_responses |= self._create_volume_cover_endpoint_responses(series)

            return self._build_response(static_responses[endpoint])

    def download_file(self, url: str) -> Optional[bytes]:
        return self._file_cache.get(url.split("/")[-1], DownloadedFile(b"", "")).data

    @staticmethod
    def _build_response(data: Dict[str, Any], status: str = "success") -> Dict[str, Any]:
        return {"result": status} | data

    @staticmethod
    def _wrap_in_data(data: Union[List[Any], Dict[str, Any]]) -> Dict[str, Any]:
        return {"data": data}

    def _get_chapter_data(self, params: Dict[str, Any]) -> Dict[str, Any]:

        if params["offset"] != 0:
            return self._wrap_in_data([])

        all_chapters = itertools.chain(*[
            series.get_chapters()
            for series in self._series
            if series.id == params["manga"]
        ])

        return self._wrap_in_data([
            self._create_chapter_response(chapter, "somegroup")
            for chapter in all_chapters
        ])

    def _create_chapter_response(self, chapter: MangaChapter, group: str) -> Dict[str, Any]:
        return {
            "id": TestIdCreator.create_chapter_id(chapter),
            "relationships": [{"type": "scanlation_group", "id": group}],
            "attributes": {
                "volume": None if chapter.volume is None else str(chapter.volume),
                "chapter": str(chapter.number),
                "title": chapter.title,
                "createdAt": chapter.published_at.strftime("%Y-%m-%dT%H:%M:%S"),
                "externalUrl": "External" if self._external_chapters else None
            }
        }

    def _create_manga_endpoint_responses(self, series: MangaSeries) -> Dict[str, Any]:
        return {
            f"manga/{series.id}": self._wrap_in_data({
                "attributes": {"title": {"en": series.name}},
                "relationships": [
                    {"type": "author", "id": TestIdCreator.create_author_id(series.author)},
                    {"type": "artist", "id": TestIdCreator.create_author_id(series.artist)}
                ]
            })
        }

    def _create_author_endpoint_responses(self, author: Optional[str]) -> Dict[str, Any]:

        if author is None:
            return {}

        return {
            f"author/{TestIdCreator.create_author_id(author)}": self._wrap_in_data(
                {"attributes": {"name": author}}
            ),
        }

    @staticmethod
    def _create_chapter_page_endpoint_responses(series: MangaSeries):
        return {
            f"at-home/server/{TestIdCreator.create_chapter_id(chapter)}": {
                "baseUrl": "example.com",
                "chapter": {
                    "hash": TestIdCreator.create_chapter_id(chapter),
                    "data": [f"{pagenumber}.png" for pagenumber in range(0, len(chapter.pages))]
                }
            } for chapter in series.get_chapters()
        }

    def _create_volume_cover_endpoint_responses(self, series: MangaSeries):
        self._file_cache = {
            volume.cover.filename: volume.cover
            for volume in series.volumes
            if volume.cover is not None
        }
        return {
            "cover": self._wrap_in_data([
                {
                    "attributes": {
                        "volume": None if volume.volume_number is None else str(volume.volume_number),
                        "fileName": volume.cover.filename
                    }
                }
                for volume in series.volumes
                if volume.cover is not None
            ])
        }
