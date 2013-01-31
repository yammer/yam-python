"""
Shared support for test cases.
"""

from mock import Mock, ANY
import requests

class HTTPHelpers(object):
    """
    Mixin providing methods for stubbing HTTP requests and asserting that
    the correct tests were made.
    """

    def setUp(self):
        self.__original_request_method = requests.request

    def tearDown(self):
        requests.request = self.__original_request_method

    def stub_get_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def assert_get_request(self, url, params=ANY, headers=ANY):
        self.assert_request("get", url, params, headers)

    def stub_post_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def assert_post_request(self, url, params=ANY, headers=ANY):
        self.assert_request("post", url, params, headers)

    def assert_request(self, method, url, params=ANY, headers=ANY):
        requests.request.assert_called_with(
            method=method,
            url=url,
            params=params,
            headers=headers,
        )
