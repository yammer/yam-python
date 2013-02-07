from unittest import TestCase
from mock import patch, Mock

from yampy import Yammer
from yampy.apis import MessagesAPI, UsersAPI

class YammerTest(TestCase):
    @patch("yampy.yammer.MessagesAPI", spec=True)
    @patch("yampy.yammer.Client", spec=True)
    def test_messages_returns_a_messages_api_instance(self, MockClient,
                                                      MockMessagesAPI):
        yammer = Yammer(access_token="abc123")
        messages = yammer.messages

        MockClient.assert_called_once_with(
            access_token="abc123",
            base_url=None,
        )
        MockMessagesAPI.assert_called_once_with(
            client=MockClient(),
        )
        self.assertIsInstance(messages, MessagesAPI)

    @patch("yampy.yammer.UsersAPI", spec=True)
    @patch("yampy.yammer.Client", spec=True)
    def test_users_returns_a_users_api_instance(self, MockClient,
                                                MockUsersAPI):
        yammer = Yammer(access_token="abc123")
        users = yammer.users

        MockClient.assert_called_once_with(
            access_token="abc123",
            base_url=None,
        )
        MockUsersAPI.assert_called_once_with(
            client=MockClient(),
        )
        self.assertIsInstance(users, UsersAPI)
