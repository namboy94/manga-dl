import json
import logging
import time
from typing import Optional, Dict, Any

import requests
from requests import Response


class HttpRequester:
    logger = logging.getLogger("HttpRequester")

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:

        response = self._perform_get(url, params)

        if response.status_code == 429:
            self.logger.warning("Rate limited, retrying in 60 seconds")
            time.sleep(60)
            response = self._perform_get(url, params)

        if response.status_code >= 300:
            self.logger.warning(f"Error {response.status_code}: {response.text}")
            return None

        return json.loads(response.text)

    def download_file(self, url: str) -> bytes:
        retry_count = 0
        max_retry = 3
        while retry_count < max_retry:
            retry_count += 1

            try:
                resp = requests.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                if resp.status_code >= 300:
                    self.logger.warning(f"Couldn't download {url}")
                else:
                    return resp.content

            except Exception as e:
                self.logger.warning(f"Failed downloading {url}")
                raise e

    @staticmethod
    def _perform_get(url: str, params: Optional[Dict[str, Any]] = None) -> Response:

        if params is None:
            params = {}
        return requests.get(url, params=params)
