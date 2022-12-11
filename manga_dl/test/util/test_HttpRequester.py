import json
from typing import Dict, Any
from unittest.mock import patch, Mock

from requests import Response

from manga_dl.util.HttpRequester import HttpRequester
from manga_dl.util.Timer import Timer


class TestHttpRequester:

    def setup_method(self):
        self.timer = Mock(Timer)
        self.timer.sleep.return_value = None
        self.under_test = HttpRequester(self.timer)

    def test_get(self):
        with patch("requests.get") as get:
            expected = {"hello": "world"}
            get.return_value = self._create_json_response(expected)

            assert self.under_test.get_json("example.com") == expected
            self.timer.sleep.assert_not_called()

    def test_get_failed(self):
        with patch("requests.get") as get:
            get.return_value = self._create_json_response({}, 404)

            assert self.under_test.get_json("example.com") is None
            self.timer.sleep.assert_not_called()

    def test_get_rate_limited_retry_success(self):
        with patch("requests.get") as get:
            expected = {"hello": "world"}
            get.side_effect = [self._create_json_response({}, 429), self._create_json_response(expected, 200)]

            assert self.under_test.get_json("example.com") == expected
            self.timer.sleep.called_with(60)
            self.timer.sleep.assert_called_once()

    def test_get_connection_error_retry_success(self):
        counter = {"count": 0}

        def get_mock(*_, **__):
            if counter["count"] == 0:
                counter["count"] += 1
                raise ConnectionError()
            return self._create_json_response(expected, 200)

        with patch("requests.get") as get:
            expected = {"hello": "world"}
            get.side_effect = get_mock

            assert self.under_test.get_json("example.com") == expected
            self.timer.sleep.called_with(60)
            self.timer.sleep.assert_called_once()

    def test_get_rate_limited_retry_failure(self):
        with patch("requests.get") as get:
            get.side_effect = [self._create_json_response({}, 429),
                               self._create_json_response({}, 429),
                               self._create_json_response({}, 200)]

            assert self.under_test.get_json("example.com") is None
            self.timer.sleep.called_with(60)
            self.timer.sleep.called_once()

    def test_download_file(self):
        with patch("requests.get") as get:
            expected = b"Hello World"
            get.return_value = self._create_binary_response(expected)

            assert self.under_test.download_file("example.com") == expected
            self.timer.sleep.assert_not_called()

    def test_download_file_failed(self):
        with patch("requests.get") as get:
            get.return_value = self._create_binary_response(b"", 404)

            assert self.under_test.download_file("example.com") is None
            self.timer.sleep.assert_not_called()

    def test_download_file_retry_success(self):
        with patch("requests.get") as get:
            expected = b"Hello World"
            get.side_effect = [self._create_binary_response(b"", 429),
                               self._create_binary_response(expected, 200)]

            assert self.under_test.download_file("example.com") == expected
            self.timer.sleep.called_with(60)
            self.timer.sleep.called_once()

    def test_download_file_retry_failed(self):
        with patch("requests.get") as get:
            get.side_effect = [self._create_binary_response(b"", 429),
                               self._create_binary_response(b"", 429),
                               self._create_binary_response(b"", 200)]

            assert self.under_test.download_file("example.com") is None
            self.timer.sleep.called_with(60)
            self.timer.sleep.called_once()

    @staticmethod
    def _create_json_response(content: Dict[str, Any], status_code: int = 200) -> Response:
        response = Mock(Response)
        response.status_code = status_code
        response.text = json.dumps(content)
        return response

    @staticmethod
    def _create_binary_response(content: bytes, status_code: int = 200) -> Response:
        response = Mock(Response)
        response.status_code = status_code
        response.content = content
        return response
