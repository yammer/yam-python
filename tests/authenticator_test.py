from unittest import TestCase

from support import HTTPHelpers

import json
from urlparse import urlparse, parse_qs

from yampy import Authenticator
from yampy.errors import *

class AuthenticatorAuthorizationUrlTest(TestCase):
    def setUp(self):
        authenticator = Authenticator(client_id="foo", client_secret="bar")
        auth_url = authenticator.authorization_url(
            redirect_uri="http://example.com/auth/callback"
        )
        self.auth_url_parts = urlparse(auth_url)

    def test_authorization_url_uses_https(self):
        self.assertEqual("https", self.auth_url_parts.scheme)

    def test_authorization_url_has_the_expected_address(self):
        self.assertEqual("www.yammer.com", self.auth_url_parts.netloc)
        self.assertEqual("/dialog/oauth", self.auth_url_parts.path)

    def test_authorization_url_has_the_expected_parameters(self):
        expected_params = {
            "client_id": ["foo"],
            "redirect_uri": ["http://example.com/auth/callback"],
        }
        params = parse_qs(self.auth_url_parts.query)
        self.assertEqual(expected_params, params)


class AuthenticatorFetchAccessDataTest(HTTPHelpers, TestCase):
    def test_fetch_access_data_returns_parsed_response_json(self):
        self.stub_get_requests(response_body=self.valid_response_json)
        authenticator = Authenticator(client_id="foo", client_secret="bar")

        response_data = authenticator.fetch_access_data("my-code")

        self.assert_get_request(
            url="https://www.yammer.com/oauth2/access_token.json",
            headers={},
            params={
                "client_id": "foo",
                "client_secret": "bar",
                "code": "my-code",
            },
        )
        self.assertEqual(self.valid_response_data, response_data)

    @property
    def valid_response_data(self):
        return {
            "user": {
                "full_name": "Joe Bloggs",
                "state": "active",
            },
            "network": {
                "name": "Acme Inc.",
                "paid": True,
            },
            "access_token": {
                "token": "abc123",
                "view_messages": True,
            },
        }

    @property
    def valid_response_json(self):
        return json.dumps(self.valid_response_data)


class AuthenticatorFetchAccessTokenTest(HTTPHelpers, TestCase):
    def test_fetch_access_token_returns_the_access_token(self):
        self.stub_get_requests(response_body=self.valid_response_json)
        authenticator = Authenticator(client_id="foo", client_secret="bar")

        access_token = authenticator.fetch_access_token("my-code")

        self.assert_get_request(
            url="https://www.yammer.com/oauth2/access_token.json",
            headers={},
            params={
                "client_id": "foo",
                "client_secret": "bar",
                "code": "my-code",
            },
        )
        self.assertEqual("abc123", access_token)

    def test_fetch_access_token_handles_an_unexpected_response_format(self):
        self.stub_get_requests(response_body="""{"foo": "bar"}""")
        authenticator = Authenticator(client_id="foo", client_secret="bar")

        self.assertRaises(ResponseError,
                          authenticator.fetch_access_token, "my-code")

    @property
    def valid_response_json(self):
        return """{
            "user": {
                "full_name": "Joe Bloggs",
                "state": "active"
            },
            "network": {
                "name": "Acme Inc.",
                "paid": true
            },
            "access_token": {
                "token": "abc123",
                "view_messages": true
            }
        }"""
