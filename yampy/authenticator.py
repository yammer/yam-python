from urllib import urlencode

from constants import DEFAULT_OAUTH_BASE_URL, DEFAULT_OAUTH_DIALOG_URL
from client import Client
from errors import ResponseError

class Authenticator(object):
    """
    Responsible for authenticating users against the Yammer API.

    The OAuth2 authentication process involves several steps:
    1. Send the user to the URL returned by authorization_url. They can use
       this page to grant your application access to their account.
    2. Yammer redirects them to the redirect_uri you provided with a code that
       can be exchanged for an access token.
    3. Exchange the code for an access token using the fetch_access_token
       method.
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def authorization_url(self, redirect_uri):
        """
        Returns the URL the user needs to visit to grant your application
        access to their Yammer account. When they are done they will be
        redirected to the redirect_uri you provide with a code that can be
        exchanged for an access token.
        """
        query = urlencode({
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
        })
        return "?".join([DEFAULT_OAUTH_DIALOG_URL, query])

    def fetch_access_data(self, code):
        """
        Returns the complete response from the Yammer API access token request.
        This is a dict with "user", "network" and "access_token" keys.

        You can access the token itself as:
            response["access_token"]["token"]

        If you only intend to make use of the token, you should use the
        fetch_access_token method instead.
        """
        client = Client(base_url=DEFAULT_OAUTH_BASE_URL)
        return client.get(
            path="/access_token",
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
        )

    def fetch_access_token(self, code):
        """
        Exchanges the given code for an access token.
        """
        access_data = self.fetch_access_data(code)
        try:
            return access_data["access_token"]["token"]
        except KeyError:
            raise ResponseError("Unexpected response format")
