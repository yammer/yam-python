"""
Shared support for test cases.
"""

from mock import Mock, ANY
import os
import requests
from unittest.case import SkipTest

def skip_without_environment_variable(variable):
    """
    Decorator for a test methods, which makes execution conditional on an
    environment variable.

    When the environment variable is set, the test is run and the value of
    the variable is passed as an argument.

    When the environment variable is not set, the test is skipped.
    """
    def decorator(test_method):
        access_token = os.getenv(variable)
        def wrapper(self):
            if access_token:
                test_method(self, access_token)
            else:
                raise SkipTest("%s is not set" % variable)
        return wrapper
    return decorator


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
