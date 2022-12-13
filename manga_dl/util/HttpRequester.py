import json
import logging
import os.path
from pathlib import Path
from typing import Optional, Dict, Any, Callable

import requests
import requests_cache
from injector import inject
from requests import Response, Session

from manga_dl.util.Timer import Timer


class HttpRequester:
    logger = logging.getLogger("HttpRequester")

    @inject
    def __init__(self, timer: Timer):
        self.timer = timer
        self.cache_file = Path(os.path.expanduser("~")) / ".cache/mangadl.sqlite"
        self.change_cache_file(self.cache_file)

    def change_cache_file(self, path: Path):
        self.cache_file = path
        self.cache_file.parent.mkdir(exist_ok=True, parents=True)
        self._create_session().close()

    def get_json(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            cached: bool = True,
            delay: float = 0.0
    ) -> Optional[Dict[str, Any]]:
        response = self._handle_request(
            lambda: self._request("GET", url, params=params, cached=cached, delay=delay)
        )
        return response if response is None else json.loads(response.text)

    def download_file(self, url: str, cached: bool = True, delay: float = 0.0) -> Optional[bytes]:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = self._handle_request(
            lambda: self._request("GET", url, headers=headers, cached=cached, delay=delay)
        )
        return response if response is None else response.content

    def _request(
            self,
            method: str,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            cached: bool = True,
            delay: float = 0.0
    ) -> Response:
        session = self._create_session(cached)
        response = session.request(method, url, params=params, headers=headers)

        if delay > 0.0 and (not cached or not response.from_cache):  # type: ignore
            self.timer.sleep(delay)

        return response

    def _handle_request(self, request_generator: Callable[[], Response]) -> Optional[Response]:

        try:
            response = request_generator()
        except ConnectionError:
            response = Response()
            response.status_code = 429

        if response.status_code == 429:
            self.logger.warning("Rate limited, retrying in 60 seconds")
            self.timer.sleep(60)
            response = request_generator()

        if response.status_code >= 300:
            self.logger.warning(f"Error {response.status_code}: {response.text}")
            return None

        return response

    def _create_session(self, cached: bool = True) -> Session:
        cache_file_path = str(self.cache_file).rsplit(".sqlite", 1)[0]
        return requests.session() if not cached else requests_cache.CachedSession(cache_file_path)
