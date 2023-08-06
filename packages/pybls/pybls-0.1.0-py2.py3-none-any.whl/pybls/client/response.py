"""Response Object Abstraction Model"""
from typing import Union


class PyBLSResponse(dict):
    """PyBLS API Wrapper Response Object Abstraction."""

    def __init__(self, data):
        super(PyBLSResponse, self).__init__(data)

    @property
    def status(self) -> Union[str, None]:
        """Access for `self.status`."""
        return self.get("status")

    @property
    def response_time(self) -> Union[int, None]:
        """Access for `self.responseTime`."""
        return self.get("responseTime")

    @property
    def message(self) -> Union[list, None]:
        """Access for `self.message`."""
        return self.get("message", [])

    @property
    def results(self) -> Union[dict, None]:
        """Access for `self.Results`."""
        return self.get("Results")
