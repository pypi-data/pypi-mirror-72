"""Mock BLS API Response Data."""
from requests import HTTPError

REQUEST_SUCCESS = {
    'status': 'REQUEST_SUCCEEDED',
    'responseTime': 98,
    'message': [],
    'Results': {
        'series': [
            {
                'seriesID': 'CEU0800000003',
                'data': [
                    {'year': '2020', 'period': 'M05', 'periodName': 'May', 'latest': 'true', 'value': '29.56',
                     'footnotes': [{'code': 'P', 'text': 'preliminary'}]},
                    {'year': '2020', 'period': 'M04', 'periodName': 'April', 'value': '30.06',
                     'footnotes': [{'code': 'P', 'text': 'preliminary'}]},
                    {'year': '2020', 'period': 'M03', 'periodName': 'March', 'value': '28.70', 'footnotes': [{}]},
                    {'year': '2020', 'period': 'M02', 'periodName': 'February', 'value': '28.64', 'footnotes': [{}]},
                    {'year': '2020', 'period': 'M01', 'periodName': 'January', 'value': '28.35', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M12', 'periodName': 'December', 'value': '28.26', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M11', 'periodName': 'November', 'value': '28.02', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M10', 'periodName': 'October', 'value': '27.93', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M09', 'periodName': 'September', 'value': '28.08', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M08', 'periodName': 'August', 'value': '27.68', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M07', 'periodName': 'July', 'value': '27.58', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M06', 'periodName': 'June', 'value': '27.66', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M05', 'periodName': 'May', 'value': '27.53', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M04', 'periodName': 'April', 'value': '27.63', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M03', 'periodName': 'March', 'value': '27.57', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M02', 'periodName': 'February', 'value': '27.58', 'footnotes': [{}]},
                    {'year': '2019', 'period': 'M01', 'periodName': 'January', 'value': '27.51', 'footnotes': [{}]}
                ]
            }
        ]
    }
}


class RequestSuccessObject(object):
    """Mock `requests.response` object."""

    def __init__(self, status: int = 200):
        self.status = status

    @staticmethod
    def json():
        """Property for `requests.response.json()`."""
        return REQUEST_SUCCESS

    def raise_for_status(self):
        """Property for `requests.response.raise_for_status()`."""
        if self.status != 200:
            raise HTTPError

        return None
