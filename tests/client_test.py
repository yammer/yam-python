from unittest import TestCase
from mock import Mock, ANY

import requests

from yampy import Client
from yampy.errors import *

class ClientTest(TestCase):
    def test_get_parses_response_json(self):
        self._stub_get_requests(
            response_body='{"messages": ["first", "second"]}',
        )
        client = Client(access_token="abc123")

        messages = client.get("/messages")

        self.assertEqual(messages, {"messages": ["first", "second"]})

    def test_get_uses_default_base_url(self):
        self._stub_get_requests()
        client = Client(access_token="abc123")

        client.get("/messages")

        self._assert_request("http://www.yammer.com/api/v1/messages.json")

    def test_get_uses_custom_base_url(self):
        self._stub_get_requests()
        client = Client(access_token="1a2bc3", base_url="http://example.com")

        client.get("/messages")

        self._assert_request("http://example.com/messages.json")

    def test_get_sends_authorization_header(self):
        self._stub_get_requests()
        client = Client(access_token="abc123")

        client.get("/users/123")

        self._assert_request(
            url="http://www.yammer.com/api/v1/users/123.json",
            headers={"Authorization": "Bearer abc123"},
        )

    def test_get_sends_query_string_parameters(self):
        self._stub_get_requests()
        client = Client(access_token="456efg")

        client.get("/users/by_email", email="user@example.com")

        self._assert_request(
            url="http://www.yammer.com/api/v1/users/by_email.json",
            params={"email": "user@example.com"},
        )

    def test_handle_invalid_access_token_responses(self):
        self._stub_get_requests(
            response_status=400,
            response_body="""{
                "error": {
                    "type": "OAuthException",
                    "message": "Error validating access token."
                 }
             }""",
        )
        client = Client(access_token="456efg")

        self.assertRaises(InvalidAccessTokenError, client.get, "/messages")

    def test_get_handles_rate_limit(self):
        self._stub_get_requests(response_status=429)
        client = Client(access_token="abc")

        self.assertRaises(RateLimitExceededError, client.get, "/user/1")

    def test_get_handles_404_responses(self):
        self._stub_get_requests(response_status=404)
        client = Client(access_token="456efg")

        self.assertRaises(NotFoundError, client.get, "/not/real")

    def test_get_handles_unexpected_http_responses(self):
        self._stub_get_requests(response_status=500)
        client = Client(access_token="abcdef")

        self.assertRaises(ResponseError, client.get, "/messages")

    def _stub_get_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.get = Mock(return_value=mock_response)

    def _assert_request(self, url, params=ANY, headers=ANY):
        requests.get.assert_called_with(url=url, params=params, headers=headers)
