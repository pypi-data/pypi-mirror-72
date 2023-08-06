"""
U.S. Bureau of Labor Statics Python Wrapper
Provides both `v1` and `v2` access

>>> pybls = PyBLS()
>>> data = pybls.timeseries(
...    series_id=["CEU0800000003"],
...    start_year="1995",
...    end_year="2020"
... )
"""
import json
from typing import Optional

import requests

from pybls.client.config import SeriesID
from pybls.client.response import PyBLSResponse


class PyBLS(object):
    """
    Instantiates a new PyBLS Client Instance.

    >>> pybls = PyBLS()

    With API (Registration) Key

    >>> pybls = PyBLS(api_key="apiKey")

    Args:
        api_key (Optional[str]): BLS Registration Key
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.bls.gov/publicAPI/{}/timeseries/data/"
        self.headers = {
            "Content-type": "application/json"
        }

    def _request(self, data: dict, version: str) -> PyBLSResponse:
        """
        Abstraction for a request wrapper for PyBLS.

        Args:
            data (dict): Data payload for POST request

        Returns:
            dict: Response from BLS Public API
        """
        response = requests.post(
            url=self.base_url.format(version),
            data=json.dumps(data),
            headers=self.headers
        )

        response.raise_for_status()
        response_object = PyBLSResponse(
            data=response.json()
        )

        return response_object

    def timeseries(
        self,
        series_id: list,
        start_year: str,
        end_year: str,
        version: str = "v2"
    ) -> dict:
        """
        Entry point for fetching `timeseries` data from BLS Public API.

        Args:
            series_id (list): List of `Series ID` for BLS Request
            start_year (str): `YYYY` style start year for BLS Request
            end_year (str): `YYYY` style end year for BLS Request
            version (str): API version for request to be made

        Returns:
            dict: Response from BLS Public API

        Raises:
            ValueError: Provided series_id not in SeriesID(Enum)
        """
        data = {
            "seriesid": series_id,
            "startyear": start_year,
            "endyear": end_year
        }

        if self.api_key:
            data.update(
                {"registrationkey": self.api_key}
            )

        for sid in series_id:
            if sid not in SeriesID.list():
                raise ValueError(
                    "Invalid Series ID: {}".format(
                        sid
                    )
                )

        return self._request(data=data, version=version)
