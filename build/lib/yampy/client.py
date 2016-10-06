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

import requests

from .constants import DEFAULT_BASE_URL
from .errors import ResponseError, NotFoundError, InvalidAccessTokenError, \
    RateLimitExceededError, UnauthorizedError
from .models import GenericModel


class Client(object):
    """
    A client for the Yammer API.
    """

    def __init__(self, access_token=None, base_url=None):
        self._access_token = access_token
        self._base_url = base_url or DEFAULT_BASE_URL

    def get(self, path, **kwargs):
        """
        Makes an HTTP GET request to the Yammer API. Any keyword arguments will
        be converted to query string parameters.

        The path should be the path of an API endpoint, e.g. "/messages"
        """
        return self._request("get", path, **kwargs)

    def post(self, path, **kwargs):
        """
        Makes an HTTP POST request to the Yammer API. Any keyword arguments
        will be sent as the body of the request.

        The path should be the path of an API endpoint, e.g. "/messages"
        """
        return self._request("post", path, **kwargs)

    def put(self, path, **kwargs):
        """
        Makes an HTTP PUT request to the Yammer API. Any keyword arguments will
        be sent as the body of the request.

        The path should be the path of an API endpoint, e.g. "/users/123"
        """
        return self._request("put", path, **kwargs)

    def delete(self, path, **kwargs):
        """
        Makes an HTTP DELETE request to the Yammer API.

        The path should be the path of an API endpoint, e.g. "/messages/123"
        """
        return self._request("delete", path, **kwargs)

    def _request(self, method, path, **kwargs):
        response = requests.request(
            method=method,
            url=self._build_url(path),
            headers=self._build_headers(),
            params=kwargs,
        )
        return self._parse_response(response)

    def _build_url(self, path):
        return self._base_url + path + ".json"

    def _build_headers(self):
        if self._access_token:
            return {
                "Authorization": "Bearer %s" % self._access_token,
            }
        else:
            return {}

    def _parse_response(self, response):
        if 200 <= response.status_code < 300:
            return self._value_for_response(response)
        else:
            raise self._exception_for_response(response)

    def _value_for_response(self, response):
        if response.text.strip():
            return GenericModel.from_json(response.text)
        else:
            return True

    def _exception_for_response(self, response):
        if response.status_code == 404:
            return NotFoundError(response.reason)
        elif response.status_code == 400 and "OAuthException" in response.text:
            return InvalidAccessTokenError(response.reason)
        elif response.status_code == 401:
            return UnauthorizedError(response.reason)
        elif response.status_code == 429:
            return RateLimitExceededError(response.reason)
        else:
            return ResponseError("%d error: %s" % (
                response.status_code, response.reason,
            ))
