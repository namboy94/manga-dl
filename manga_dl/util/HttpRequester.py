import json
import logging
from typing import Optional, Dict, Any, Callable

import requests
from injector import inject
from requests import Response

from manga_dl.util.Timer import Timer


class HttpRequester:
    logger = logging.getLogger("HttpRequester")

    @inject
    def __init__(self, timer: Timer):
        self.timer = timer

    def get_json(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        params = params if params is not None else {}
        response = self._handle_request(lambda: requests.get(url, params=params))
        return response if response is None else json.loads(response.text)

    def download_file(self, url: str) -> Optional[bytes]:

        headers = {"User-Agent": "Mozilla/5.0"}
        response = self._handle_request(lambda: requests.get(url, headers=headers))
        return response if response is None else response.content

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
