from apis import MessagesAPI
from client import Client

class Yammer(object):
    """
    Main entry point for accessing the Yammer API.

    Essentially this is just a Factory class that provides instances of various
    classes that interact directly with the API. For example, the messages
    method returns a MessagesAPI object.
    """

    def __init__(self, access_token=None, base_url=None):
        self._client = Client(access_token=access_token, base_url=base_url)

    @property
    def messages(self):
        """
        Returns a MessagesAPI object which can be used to call the Yammer API's
        message-related endpoints.
        """
        return MessagesAPI(client=self._client)
