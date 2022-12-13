import json
import tempfile
import time
from pathlib import Path
from typing import Dict, Any
from unittest.mock import patch, Mock

from requests import Response, Session

from manga_dl.util.HttpRequester import HttpRequester
from manga_dl.util.Timer import Timer


class TestHttpRequester:

    def setup_method(self):
        self.cache_file = tempfile.NamedTemporaryFile()
        self.timer = Mock(Timer)
        self.timer.sleep.return_value = None
        self.under_test = HttpRequester(self.timer)
        self.under_test.change_cache_file(Path(self.cache_file.name))

    def teardown_method(self):
        self.cache_file.close()

    def test_cache_file_created(self):
        directory = tempfile.TemporaryDirectory()
        directory_path = Path(directory.name)
        cache_file_path = directory_path / "subdir/cache.sqlite"

        HttpRequester(self.timer).change_cache_file(cache_file_path)

        assert cache_file_path.parent.is_dir()
        assert cache_file_path.is_file()

        directory.cleanup()

    def test_get(self, to_patch: str = "requests.session", cached: bool = False):
        with patch(to_patch) as sessionmaker:
            expected = {"hello": "world"}
            session = self._create_json_response_session(expected)
            sessionmaker.return_value = session

            assert self.under_test.get_json("example.com", cached=cached) == expected
            session.request.assert_called_with("GET", "example.com", params=None, headers=None)
            self.timer.sleep.assert_not_called()

    def test_get_cached(self):
        self.test_get("requests_cache.CachedSession", True)

    def test_get_failed(self):
        with patch("requests_cache.CachedSession") as sessionmaker:
            sessionmaker.return_value = self._create_json_response_session({}, 404)

            assert self.under_test.get_json("example.com") is None
            self.timer.sleep.assert_not_called()

    def test_get_rate_limited_retry_success(self):
        with patch("requests_cache.CachedSession") as sessionmaker:
            expected = {"hello": "world"}
            sessionmaker.side_effect = [
                self._create_json_response_session({}, 429),
                self._create_json_response_session(expected, 200)
            ]

            assert self.under_test.get_json("example.com") == expected
            self.timer.sleep.called_with(60)
            self.timer.sleep.assert_called_once()

    def test_get_connection_error_retry_success(self):
        counter = {"count": 0}

        def get_mock(*_, **__):
            if counter["count"] == 0:
                counter["count"] += 1
                raise ConnectionError()
            return self._create_json_response_session(expected, 200)

        with patch("requests_cache.CachedSession") as sessionmaker:
            expected = {"hello": "world"}
            sessionmaker.side_effect = get_mock

            assert self.under_test.get_json("example.com") == expected
            self.timer.sleep.called_with(60)
            self.timer.sleep.assert_called_once()

    def test_get_rate_limited_retry_failure(self):
        with patch("requests_cache.CachedSession") as sessionmaker:
            sessionmaker.side_effect = [
                self._create_json_response_session({}, 429),
                self._create_json_response_session({}, 429),
                self._create_json_response_session({}, 200)
            ]

            assert self.under_test.get_json("example.com") is None
            self.timer.sleep.called_with(60)
            self.timer.sleep.called_once()

    def test_download_file(self, to_patch: str = "requests.session", cached: bool = False):
        with patch(to_patch) as sessionmaker:
            expected = b"Hello World"
            session = self._create_binary_response_session(expected)
            sessionmaker.return_value = session

            assert self.under_test.download_file("example.com", cached=cached) == expected
            session.request.assert_called_with("GET", "example.com", headers={"User-Agent": "Mozilla/5.0"}, params=None)
            self.timer.sleep.assert_not_called()

    def test_download_file_cached(self):
        self.test_download_file("requests_cache.CachedSession", True)

    def test_download_file_failed(self):
        with patch("requests_cache.CachedSession") as sessionmaker:
            sessionmaker.return_value = self._create_binary_response_session(b"", 404)

            assert self.under_test.download_file("example.com") is None
            self.timer.sleep.assert_not_called()

    def test_download_file_retry_success(self):
        with patch("requests_cache.CachedSession") as sessionmaker:
            expected = b"Hello World"
            sessionmaker.side_effect = [self._create_binary_response_session(b"", 429),
                                        self._create_binary_response_session(expected, 200)]

            assert self.under_test.download_file("example.com") == expected
            self.timer.sleep.called_with(60)
            self.timer.sleep.called_once()

    def test_download_file_retry_failed(self):
        with patch("requests_cache.CachedSession") as sessionmaker:
            sessionmaker.side_effect = [self._create_binary_response_session(b"", 429),
                                        self._create_binary_response_session(b"", 429),
                                        self._create_binary_response_session(b"", 200)]

            assert self.under_test.download_file("example.com") is None
            self.timer.sleep.called_with(60)
            self.timer.sleep.called_once()

    def test_request_chache(self):
        url = "https://jsonplaceholder.typicode.com/todos/"
        time_anchor = time.time()
        expected = self.under_test.get_json(url)

        initial_delta = time.time() - time_anchor
        time_anchor = time.time()

        for x in range(20):
            self.under_test.get_json(url)
        cached_delta = time.time() - time_anchor

        assert initial_delta > cached_delta
        assert expected == self.under_test.get_json(url)

    def test_uncached_delay(self):
        with patch("requests.session") as sessionmaker:
            sessionmaker.return_value = self._create_json_response_session({})

            self.under_test.get_json("example.com", cached=False, delay=100.0)

            self.timer.sleep.assert_called_with(100.0)

    def test_uncached_delay_zero(self):
        with patch("requests.session") as sessionmaker:
            sessionmaker.return_value = self._create_json_response_session({})

            self.under_test.get_json("example.com", cached=False, delay=0.0)

            self.timer.sleep.assert_not_called()

    def test_cached_delay_miss(self):
        with patch("requests_cache.CachedSession") as sessionmaker:
            sessionmaker.return_value = self._create_json_response_session({})

            self.under_test.get_json("example.com", cached=True, delay=100.0)

            self.timer.sleep.assert_called_with(100.0)

    def test_cached_delay_hit(self):
        with patch("requests_cache.CachedSession") as sessionmaker:
            sessionmaker.return_value = self._create_json_response_session({}, was_cached=True)

            self.under_test.get_json("example.com", cached=True, delay=100.0)

            self.timer.sleep.assert_not_called()

    def _create_json_response_session(
            self,
            content: Dict[str, Any],
            status_code: int = 200,
            was_cached: bool = False
    ) -> Mock:
        response = self._create_response(status_code, was_cached)
        response.text = json.dumps(content)
        return self._create_session(response)

    def _create_binary_response_session(
            self,
            content: bytes,
            status_code: int = 200,
            was_cached: bool = False
    ) -> Mock:
        response = self._create_response(status_code, was_cached)
        response.content = content
        return self._create_session(response)

    @staticmethod
    def _create_response(status_code: int, was_cached: bool) -> Mock:
        response = Mock(Response)
        response.status_code = status_code
        response.from_cache = was_cached
        return response

    @staticmethod
    def _create_session(return_value: Response) -> Mock:
        session = Mock(Session)
        session.request.return_value = return_value
        return session
