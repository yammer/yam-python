from unittest import TestCase

from urlparse import urlparse, parse_qs

from yampy import Authenticator

class AuthenticatorAuthorizationUrlTest(TestCase):
    def setUp(self):
        authenticator = Authenticator(client_id="foo", client_secret="bar")
        auth_url = authenticator.authorization_url(
            return_uri="http://example.com/auth/callback"
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
            "return_uri": ["http://example.com/auth/callback"],
        }
        params = parse_qs(self.auth_url_parts.query)
        self.assertEqual(expected_params, params)
