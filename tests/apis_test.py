from mock import Mock
from unittest import TestCase

from yampy.apis import MessagesAPI

class MessagesAPIMessageListFetchingTest(TestCase):
    """
    Tests all MessagesAPI methods associated with fetching lists of messages.
    """

    def setUp(self):
        self.mock_get_response = Mock()
        self.mock_client = Mock()
        self.mock_client.get.return_value = self.mock_get_response
        self.messages_api = MessagesAPI(client=self.mock_client)

    def test_all(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.all(**kwargs)

            self.mock_client.get.assert_called_with("/messages", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_from_my_feed(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.from_my_feed(**kwargs)

            self.mock_client.get.assert_called_with("/messages/my_feed", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_from_top_conversations(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.from_top_conversations(**kwargs)

            self.mock_client.get.assert_called_with("/messages/algo", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_from_followed_conversations(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.from_followed_conversations(**kwargs)

            self.mock_client.get.assert_called_with("/messages/following", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_sent(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.sent(**kwargs)

            self.mock_client.get.assert_called_with("/messages/sent", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_private(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.private(**kwargs)

            self.mock_client.get.assert_called_with("/messages/private", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_received(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.received(**kwargs)

            self.mock_client.get.assert_called_with("/messages/received", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    @property
    def valid_message_list_arguments(self):
        return (
            {},
            {"older_than": 12345},
            {"newer_than": 54321},
            {"limit": 30},
            {"threaded": "true"},
            {"threaded": "extended"},
        )
