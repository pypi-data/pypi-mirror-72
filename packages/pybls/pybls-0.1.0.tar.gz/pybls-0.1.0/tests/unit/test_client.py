"""Unit Tests for `bls` Module."""
from unittest import TestCase

import mock
import pytest
import requests
from mock import MagicMock
from requests import HTTPError

from pybls.client.bls import PyBLS
from tests.data.mock_response import RequestSuccessObject


class TestPyBLS(TestCase):
    """Unit test cases for PyBLS."""

    def setUp(self) -> None:
        """Instantiate PyBLS."""
        self.client = PyBLS(api_key="you-will-never-guess")

    @mock.patch.object(requests, "post")
    def test_request_success(self, mock_requests: MagicMock):
        """Unit test case for `_request(...)` success."""
        mock_requests.return_value = RequestSuccessObject()

        response = self.client._request(
            data={
                "seriesid": "1234",
                "startyear": "1995",
                "endyear": "2005"
            },
            version="v2"
        )

        assert isinstance(response, dict)

    @mock.patch.object(requests, "post")
    def test_request_raises(self, mock_requests: MagicMock):
        """Unit test case for `_request(...)` raises."""
        mock_requests.return_value = RequestSuccessObject(status=404)

        with pytest.raises(HTTPError):
            self.client._request(
                data={
                    "seriesid": "1234",
                    "startyear": "1995",
                    "endyear": "2005"
                },
                version="v2"
            )

    @mock.patch.object(requests, "post")
    def test_timeseries_success(self, mock_requests: MagicMock):
        """Unit test case for `timeseries(...)` success."""
        mock_requests.return_value = RequestSuccessObject()

        response = self.client.timeseries(
            series_id=["CEU0800000003"],
            start_year="1995",
            end_year="2020"
        )

        assert isinstance(response, dict)

    def test_timeseries_raises(self):
        """Unit test case for `timeseries(...)` raises."""
        with pytest.raises(ValueError):
            self.client.timeseries(
                series_id=["123"],
                start_year="1995",
                end_year="2020"
            )
