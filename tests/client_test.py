from unittest import TestCase
from mock import Mock, ANY

import requests

from yampy import Client
from yampy.errors import *

class HTTPHelpers(object):
    def _stub_get_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def _assert_get_request(self, url, params=ANY, headers=ANY):
        self._assert_request("get", url, params, headers)

    def _stub_post_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def _assert_post_request(self, url, params=ANY, headers=ANY):
        self._assert_request("post", url, params, headers)

    def _assert_request(self, method, url, params=ANY, headers=ANY):
        requests.request.assert_called_with(
            method=method,
            url=url,
            params=params,
            headers=headers,
        )


class ClientGetTest(TestCase, HTTPHelpers):
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

        self._assert_get_request("http://www.yammer.com/api/v1/messages.json")

    def test_get_uses_custom_base_url(self):
        self._stub_get_requests()
        client = Client(access_token="1a2bc3", base_url="http://example.com")

        client.get("/messages")

        self._assert_get_request("http://example.com/messages.json")

    def test_get_sends_authorization_header(self):
        self._stub_get_requests()
        client = Client(access_token="abc123")

        client.get("/users/123")

        self._assert_get_request(
            url="http://www.yammer.com/api/v1/users/123.json",
            headers={"Authorization": "Bearer abc123"},
        )

    def test_get_sends_query_string_parameters(self):
        self._stub_get_requests()
        client = Client(access_token="456efg")

        client.get("/users/by_email", email="user@example.com")

        self._assert_get_request(
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


class ClientPostTest(TestCase, HTTPHelpers):
    def test_post_parses_response_json(self):
        self._stub_post_requests(
            response_body='{"messages": ["first", "second"]}',
        )
        client = Client(access_token="abc123")

        messages = client.post("/messages", body="Hello world")

        self.assertEqual(messages, {"messages": ["first", "second"]})

    def test_post_uses_default_base_url(self):
        self._stub_post_requests()
        client = Client(access_token="abc123")

        client.post("/messages", body="Hello Yammer")

        self._assert_post_request("http://www.yammer.com/api/v1/messages.json")

    def test_post_uses_custom_base_url(self):
        self._stub_post_requests()
        client = Client(access_token="1a2bc3", base_url="http://example.com")

        client.post("/messages", body="Hello fake Yammer")

        self._assert_post_request("http://example.com/messages.json")

    def test_post_sends_authorization_header(self):
        self._stub_post_requests()
        client = Client(access_token="abc123")

        client.post("/messages", body="I am authorized")

        self._assert_post_request(
            url="http://www.yammer.com/api/v1/messages.json",
            headers={"Authorization": "Bearer abc123"},
        )

    def test_post_sends_query_string_parameters(self):
        self._stub_post_requests()
        client = Client(access_token="456efg")

        client.post("/messages", body="Oh hai")

        self._assert_post_request(
            url="http://www.yammer.com/api/v1/messages.json",
            params={"body": "Oh hai"},
        )

    def test_handle_invalid_access_token_responses(self):
        self._stub_post_requests(
            response_status=400,
            response_body="""{
                "error": {
                    "type": "OAuthException",
                    "message": "Error validating access token."
                 }
             }""",
        )
        client = Client(access_token="456efg")

        self.assertRaises(InvalidAccessTokenError, client.post, "/messages",
                          body="No more token")

    def test_post_handles_rate_limit(self):
        self._stub_post_requests(response_status=429)
        client = Client(access_token="abc")

        self.assertRaises(RateLimitExceededError, client.post, "/messages",
                          body="Do I talk too much?")

    def test_post_handles_404_responses(self):
        self._stub_post_requests(response_status=404)
        client = Client(access_token="456efg")

        self.assertRaises(NotFoundError, client.post, "/not/real")

    def test_post_handles_unexpected_http_responses(self):
        self._stub_post_requests(response_status=500)
        client = Client(access_token="abcdef")

        self.assertRaises(ResponseError, client.post, "/messages",
                          body="BOOM!")
