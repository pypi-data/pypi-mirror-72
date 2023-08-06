"""Unit Tests for `response` Module."""
from unittest import TestCase

from pybls.client.response import PyBLSResponse

from tests.data.mock_response import REQUEST_SUCCESS


class TestPyBLSResponse(TestCase):
    """Unit test cases for PyBLSResponse."""

    def setUp(self) -> None:
        """Instantiate PyBLSResponse."""
        self.response = PyBLSResponse(data=REQUEST_SUCCESS)

    def test_status(self):
        """Unit test case for `status`."""
        assert self.response.status == "REQUEST_SUCCEEDED"

    def test_response_time(self):
        """Unit test case for `responseTime`."""
        assert self.response.response_time == 98

    def test_message(self):
        """Unit test case for `message`."""
        assert self.response.message == []

    def test_results(self):
        """Unit test case for `results`."""
        assert isinstance(self.response.results, dict)
