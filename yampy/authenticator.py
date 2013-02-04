from urllib import urlencode

class Authenticator(object):
    """
    Responsible for authenticating users against the Yammer API.

    The OAuth2 authentication process involves several steps:
    1. Send the user to the URL returned by authorization_url. They can use
       this page to grant your application access to their account.
    2. Yammer redirects them to the return_uri you provided with a code that
       can be exchanged for an access token.
    3. Exchange the code for an access token using the fetch_access_token
       method.
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id

    def authorization_url(self, return_uri):
        """
        Returns the URL the user needs to visit to grant your application
        access to their Yammer account. When they are done they will be
        redirected to the return_uri you provide with a code that can be
        exchanged for an access token.
        """
        return "https://www.yammer.com/dialog/oauth?%s" % urlencode({
            "client_id": self.client_id,
            "return_uri": return_uri,
        })
