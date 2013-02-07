import json
from unittest import TestCase
from urlparse import urlparse, parse_qs

from support.unit import HTTPHelpers
from yampy import Authenticator
from yampy.errors import *

class AuthenticatorAuthorizationUrlTest(TestCase):
    def test_authorization_url_using_the_default_oauth_dialog_url(self):
        authenticator = Authenticator(
            client_id="foo",
            client_secret="bar",
        )
        auth_url_parts, params = self.parsed_authorization_url(authenticator)

        self.assertEqual("https", auth_url_parts.scheme)
        self.assertEqual("www.yammer.com", auth_url_parts.netloc)
        self.assertEqual("/dialog/oauth", auth_url_parts.path)
        self.assertEqual(
            {
                "client_id": ["foo"],
                "redirect_uri": ["http://example.com/auth/callback"],
            },
            params,
        )

    def test_authorization_url_can_use_a_custom_oauth_dialog_url(self):
        authenticator = Authenticator(
            client_id="my-client-id",
            client_secret="bar",
            oauth_dialog_url="http://example.com/test/dialog",
        )
        auth_url_parts, params = self.parsed_authorization_url(authenticator)

        self.assertEqual("http", auth_url_parts.scheme)
        self.assertEqual("example.com", auth_url_parts.netloc)
        self.assertEqual("/test/dialog", auth_url_parts.path)
        self.assertEqual(
            {
                "client_id": ["my-client-id"],
                "redirect_uri": ["http://example.com/auth/callback"],
            },
            params,
        )

    def parsed_authorization_url(self, authenticator):
        auth_url = authenticator.authorization_url(
            redirect_uri="http://example.com/auth/callback",
        )
        auth_url_parts = urlparse(auth_url)
        params = parse_qs(auth_url_parts.query)

        return (auth_url_parts, params)


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

    def test_fetch_access_data_can_use_a_custom_oauth_url(self):
        self.stub_get_requests(response_body=self.valid_response_json)
        authenticator = Authenticator(
            client_id="foo",
            client_secret="bar",
            oauth_base_url="http://example.com/oauth",
        )

        authenticator.fetch_access_data("some-code")

        self.assert_get_request("http://example.com/oauth/access_token.json")

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
