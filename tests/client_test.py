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

from unittest import TestCase

from .support.unit import HTTPHelpers
from yampy import Client
from yampy.errors import *


class ClientGetTest(HTTPHelpers, TestCase):
    def test_get_parses_response_json(self):
        self.stub_get_requests(
            response_body='{"messages": ["first", "second"]}',
        )
        client = Client(access_token="abc123")

        messages = client.get("/messages")

        self.assertEqual(messages.messages, ["first", "second"])

    def test_get_uses_default_base_url(self):
        self.stub_get_requests()
        client = Client(access_token="abc123")

        client.get("/messages")

        self.assert_get_request("https://www.yammer.com/api/v1/messages.json")

    def test_get_uses_custom_base_url(self):
        self.stub_get_requests()
        client = Client(access_token="1a2bc3", base_url="https://example.com")

        client.get("/messages")

        self.assert_get_request("https://example.com/messages.json")

    def test_get_sends_authorization_header(self):
        self.stub_get_requests()
        client = Client(access_token="abc123")

        client.get("/users/123")

        self.assert_get_request(
            url="https://www.yammer.com/api/v1/users/123.json",
            headers={"Authorization": "Bearer abc123"},
        )

    def test_get_does_not_send_authorization_header_with_no_token(self):
        self.stub_get_requests()
        client = Client(access_token=None)

        client.get("/messages")

        self.assert_get_request(
            url="https://www.yammer.com/api/v1/messages.json",
            headers={},
        )

    def test_get_sends_query_string_parameters(self):
        self.stub_get_requests()
        client = Client(access_token="456efg")

        client.get("/users/by_email", email="user@example.com")

        self.assert_get_request(
            url="https://www.yammer.com/api/v1/users/by_email.json",
            params={"email": "user@example.com"},
        )

    def test_get_handles_invalid_access_token_responses(self):
        self.stub_get_requests(
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

    def test_get_handles_unauthorized_responses(self):
        self.stub_get_requests(response_status=401)
        client = Client(access_token="456efg")

        self.assertRaises(UnauthorizedError, client.get, "/messages")

    def test_get_handles_rate_limit_error_responses(self):
        self.stub_get_requests(response_status=429)
        client = Client(access_token="abc")

        self.assertRaises(RateLimitExceededError, client.get, "/user/1")

    def test_get_handles_not_found_responses(self):
        self.stub_get_requests(response_status=404)
        client = Client(access_token="456efg")

        self.assertRaises(NotFoundError, client.get, "/not/real")

    def test_get_handles_unexpected_http_responses(self):
        self.stub_get_requests(response_status=500)
        client = Client(access_token="abcdef")

        self.assertRaises(ResponseError, client.get, "/messages")


class ClientPostTest(HTTPHelpers, TestCase):
    def test_post_parses_response_json(self):
        self.stub_post_requests(
            response_body='{"messages": ["first", "second"]}',
        )
        client = Client(access_token="abc123")

        messages = client.post("/messages", body="Hello world")

        self.assertEqual(messages.messages, ["first", "second"])

    def test_post_uses_default_base_url(self):
        self.stub_post_requests()
        client = Client(access_token="abc123")

        client.post("/messages", body="Hello Yammer")

        self.assert_post_request("https://www.yammer.com/api/v1/messages.json")

    def test_post_uses_custom_base_url(self):
        self.stub_post_requests()
        client = Client(access_token="1a2bc3", base_url="http://example.com")

        client.post("/messages", body="Hello fake Yammer")

        self.assert_post_request("http://example.com/messages.json")

    def test_post_sends_authorization_header(self):
        self.stub_post_requests()
        client = Client(access_token="abc123")

        client.post("/messages", body="I am authorized")

        self.assert_post_request(
            url="https://www.yammer.com/api/v1/messages.json",
            headers={"Authorization": "Bearer abc123"},
        )

    def test_post_sends_query_string_parameters(self):
        self.stub_post_requests()
        client = Client(access_token="456efg")

        client.post("/messages", body="Oh hai")

        self.assert_post_request(
            url="https://www.yammer.com/api/v1/messages.json",
            params={"body": "Oh hai"},
        )

    def test_post_handles_invalid_access_token_responses(self):
        self.stub_post_requests(
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

    def test_post_handles_created_responses(self):
        self.stub_post_requests(
            response_status=201,
            response_body='{"status": "OK"}',
        )
        client = Client(access_token="456efg")

        response = client.post("/messages", body="A-OK")

        self.assertEqual(response, {"status": "OK"})

    def test_post_handles_rate_limit_error_responses(self):
        self.stub_post_requests(response_status=429)
        client = Client(access_token="abc")

        self.assertRaises(RateLimitExceededError, client.post, "/messages",
                          body="Do I talk too much?")

    def test_post_handles_not_found_responses(self):
        self.stub_post_requests(response_status=404)
        client = Client(access_token="456efg")

        self.assertRaises(NotFoundError, client.post, "/not/real")

    def test_post_handles_unexpected_http_responses(self):
        self.stub_post_requests(response_status=122)
        client = Client(access_token="abcdef")

        self.assertRaises(ResponseError, client.post, "/messages",
                          body="BOOM!")


class ClientDeleteTest(HTTPHelpers, TestCase):
    def test_delete_parses_response_json(self):
        self.stub_delete_requests(
            response_body='{"deleted": true}',
        )
        client = Client(access_token="abc123")

        response = client.delete("/messages/1")

        self.assertEqual(response.deleted, True)

    def test_delete_handles_success_with_a_blank_body(self):
        self.stub_delete_requests(response_status=200, response_body=" ")
        client = Client(access_token="foobar")

        response = client.delete("/messages/123")

        self.assertEquals(response, True)

    def test_delete_uses_default_base_url(self):
        self.stub_delete_requests()
        client = Client(access_token="abc123")

        client.delete("/messages/1")

        self.assert_delete_request("https://www.yammer.com/api/v1/messages/1.json")

    def test_delete_uses_custom_base_url(self):
        self.stub_delete_requests()
        client = Client(access_token="1a2bc3", base_url="https://example.com")

        client.delete("/messages/3")

        self.assert_delete_request("https://example.com/messages/3.json")

    def test_delete_sends_authorization_header(self):
        self.stub_delete_requests()
        client = Client(access_token="abc123")

        client.delete("/users/123")

        self.assert_delete_request(
            url="https://www.yammer.com/api/v1/users/123.json",
            headers={"Authorization": "Bearer abc123"},
        )

    def test_delete_sends_query_string_parameters(self):
        self.stub_delete_requests()
        client = Client(access_token="456efg")

        client.delete("/messages/liked_by/current", message_id=12345)

        self.assert_delete_request(
            url="https://www.yammer.com/api/v1/messages/liked_by/current.json",
            params={"message_id": 12345},
        )

    def test_delete_does_not_send_authorization_header_with_no_token(self):
        self.stub_delete_requests()
        client = Client(access_token=None)

        client.delete("/messages/14")

        self.assert_delete_request(
            url="https://www.yammer.com/api/v1/messages/14.json",
            headers={},
        )

    def test_delete_handles_invalid_access_token_responses(self):
        self.stub_delete_requests(
            response_status=400,
            response_body="""{
                "error": {
                    "type": "OAuthException",
                    "message": "Error validating access token."
                 }
             }""",
        )
        client = Client(access_token="456efg")

        self.assertRaises(InvalidAccessTokenError, client.delete, "/messages/1")

    def test_delete_handles_unauthorized_responses(self):
        self.stub_delete_requests(response_status=401)
        client = Client(access_token="456efg")

        self.assertRaises(UnauthorizedError, client.delete, "/messages/1")

    def test_delete_handles_rate_limit_error_responses(self):
        self.stub_delete_requests(response_status=429)
        client = Client(access_token="abc")

        self.assertRaises(RateLimitExceededError, client.delete, "/user/1")

    def test_delete_handles_not_found_responses(self):
        self.stub_delete_requests(response_status=404)
        client = Client(access_token="456efg")

        self.assertRaises(NotFoundError, client.delete, "/not/real")

    def test_delete_handles_unexpected_http_responses(self):
        self.stub_delete_requests(response_status=500)
        client = Client(access_token="abcdef")

        self.assertRaises(ResponseError, client.delete, "/messages/1")


class ClientPutTest(HTTPHelpers, TestCase):
    def test_put_parses_response_json(self):
        self.stub_put_requests(
            response_body='{"messages": ["first", "second"]}',
        )
        client = Client(access_token="abc123")

        messages = client.put("/messages", body="Hello world")

        self.assertEqual(messages.messages, ["first", "second"])

    def test_put_uses_default_base_url(self):
        self.stub_put_requests()
        client = Client(access_token="abc123")

        client.put("/messages", body="Hello Yammer")

        self.assert_put_request("https://www.yammer.com/api/v1/messages.json")

    def test_put_uses_custom_base_url(self):
        self.stub_put_requests()
        client = Client(access_token="1a2bc3", base_url="http://example.com")

        client.put("/messages", body="Hello fake Yammer")

        self.assert_put_request("http://example.com/messages.json")

    def test_put_sends_authorization_header(self):
        self.stub_put_requests()
        client = Client(access_token="abc123")

        client.put("/messages", body="I am authorized")

        self.assert_put_request(
            url="https://www.yammer.com/api/v1/messages.json",
            headers={"Authorization": "Bearer abc123"},
        )

    def test_put_sends_query_string_parameters(self):
        self.stub_put_requests()
        client = Client(access_token="456efg")

        client.put("/messages", body="Oh hai")

        self.assert_put_request(
            url="https://www.yammer.com/api/v1/messages.json",
            params={"body": "Oh hai"},
        )

    def test_put_handles_invalid_access_token_responses(self):
        self.stub_put_requests(
            response_status=400,
            response_body="""{
                "error": {
                    "type": "OAuthException",
                    "message": "Error validating access token."
                 }
             }""",
        )
        client = Client(access_token="456efg")

        self.assertRaises(InvalidAccessTokenError, client.put, "/messages",
                          body="No more token")

    def test_put_handles_created_responses(self):
        self.stub_put_requests(
            response_status=201,
            response_body='{"status": "OK"}',
        )
        client = Client(access_token="456efg")

        response = client.put("/messages", body="A-OK")

        self.assertEqual(response, {"status": "OK"})

    def test_put_handles_rate_limit_error_responses(self):
        self.stub_put_requests(response_status=429)
        client = Client(access_token="abc")

        self.assertRaises(RateLimitExceededError, client.put, "/messages",
                          body="Do I talk too much?")

    def test_put_handles_not_found_responses(self):
        self.stub_put_requests(response_status=404)
        client = Client(access_token="456efg")

        self.assertRaises(NotFoundError, client.put, "/not/real")

    def test_put_handles_unexpected_http_responses(self):
        self.stub_put_requests(response_status=122)
        client = Client(access_token="abcdef")

        self.assertRaises(ResponseError, client.put, "/messages",
                          body="BOOM!")
