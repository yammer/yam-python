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

try:
    from urllib.parse import urlencode  # Python 3
except ImportError:
    from urllib import urlencode        # Python 2

from .constants import DEFAULT_OAUTH_BASE_URL, DEFAULT_OAUTH_DIALOG_URL
from .client import Client
from .errors import ResponseError

class Authenticator(object):
    """
    Responsible for authenticating users against the Yammer API.

    The OAuth2 authentication process involves several steps:

    1. Send the user to the URL returned by ``authorization_url``. They can use
       this page to grant your application access to their account.
    2. Yammer redirects them to the ``redirect_uri`` you provided with a code
       that can be exchanged for an access token.
    3. Exchange the code for an access token using the ``fetch_access_token``
       method.
    """

    def __init__(self, client_id, client_secret,
                 oauth_dialog_url=None, oauth_base_url=None):
        """
        Initializes a new Authenticator. The client_id and client_secret
        identify your application, you acquire them when registering your
        application with Yammer. See http://www.yammer.com/client_applications

        Keyword arguments can be used to modify the URLs generated in this
        class, e.g. to avoid hitting the live API from a client application's
        test suite. Pass None to use the default URLs.

        * ``oauth_dialog_url`` -- The URL the user must visit to authorize the
          application. Used by the authorization_url method.
        * ``oauth_base_url`` -- The base URL for OAuth API requests, e.g. token
          exchange. Used by ``fetch_access_data`` or ``fetch_access_token``.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._oauth_dialog_url = oauth_dialog_url or DEFAULT_OAUTH_DIALOG_URL
        self._oauth_base_url = oauth_base_url or DEFAULT_OAUTH_BASE_URL

    def authorization_url(self, redirect_uri):
        """
        Returns the URL the user needs to visit to grant your application
        access to their Yammer account. When they are done they will be
        redirected to the ``redirect_uri`` you provide with a code that can be
        exchanged for an access token.
        """
        query = urlencode({
            "client_id": self._client_id,
            "redirect_uri": redirect_uri,
        })
        return "?".join([self._oauth_dialog_url, query])

    def fetch_access_data(self, code):
        """
        Returns the complete response from the Yammer API access token request.
        This is a dict with "user", "network" and "access_token" keys.

        You can access the token itself as: ``response.access_token.token``

        If you only intend to make use of the token, you can use the
        ``fetch_access_token`` method instead for convenience.
        """
        client = Client(base_url=self._oauth_base_url)
        return client.get(
            path="/access_token",
            client_id=self._client_id,
            client_secret=self._client_secret,
            code=code,
        )

    def fetch_access_token(self, code):
        """
        Convenience method to exchange a code for an access token, discarding
        the other user and network data that the Yammer API returns with the
        access token.

        If you require user and network information, you should use the
        ``fetch_access_data`` method instead.
        """
        access_data = self.fetch_access_data(code)
        try:
            return access_data.access_token.token
        except AttributeError:
            raise ResponseError("Unexpected response format")
