# Copyright (c) Microsoft Corporation
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY
# IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR
# PURPOSE, MERCHANTABLITY OR NON-INFRINGEMENT.
#
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.

"""
Shared support for unit tests.
"""

from mock import Mock, ANY
import requests
from unittest import TestCase


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

    def stub_delete_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def assert_delete_request(self, url, params=ANY, headers=ANY):
        self.assert_request("delete", url, params, headers)

    def stub_put_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def assert_put_request(self, url, params=ANY, headers=ANY):
        self.assert_request("put", url, params, headers)

    def assert_request(self, method, url, params=ANY, headers=ANY):
        requests.request.assert_called_with(
            method=method,
            url=url,
            params=params,
            headers=headers,
        )


class TestCaseWithMockClient(TestCase):
    """
    Test case with a mock yampy.Client instance.

    Use self.mock_client in place of a real Client instance. Assert values were
    returned by the mock client by checking against self.mock_get_response, etc.
    """

    def setUp(self):
        self.mock_get_response = Mock()
        self.mock_post_response = Mock()
        self.mock_delete_response = Mock()
        self.mock_put_response = Mock()
        self.mock_client = Mock()
        self.mock_client.get.return_value = self.mock_get_response
        self.mock_client.post.return_value = self.mock_post_response
        self.mock_client.delete.return_value = self.mock_delete_response
        self.mock_client.put.return_value = self.mock_put_response
