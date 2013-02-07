"""
Tests for excercising the whole system in concert.
"""

from support.integration import TestCaseWithFakeYammerServer
import yampy


class AuthenticationIntegrationTest(TestCaseWithFakeYammerServer):
    def test_authentication(self):
        authenticator = yampy.Authenticator(
            client_id="valid_client_id",
            client_secret="valid_client_secret",
            oauth_base_url="http://localhost:5000/oauth2",
        )

        access_token = authenticator.fetch_access_token("valid_code")
        self.assertEqual("valid_token", access_token)


class MessageIntegrationTest(TestCaseWithFakeYammerServer):
    def setUp(self):
        super(MessageIntegrationTest, self).setUp()
        self.yammer = yampy.Yammer(
            access_token="valid_token",
            base_url="http://localhost:5000/api/v1",
        )

    def test_fetching_messages(self):
        message_result = self.yammer.messages.all()

        self.assertEqual(3, len(message_result["messages"]))

    def test_creating_a_message(self):
        message_result = self.yammer.messages.create(
            body="Hello everyone!",
            topics=["python", "testing"],
            group_id=345,
        )

        self.assertEqual(1, len(message_result["messages"]))
        message = message_result["messages"][0]

        self.assertEqual("Hello everyone!", message["body"]["plain"])

    def test_deleting_a_message(self):
        message_result = self.yammer.messages.all()
        msg_id = message_result["messages"][0]["id"]

        deletion_result = self.yammer.messages.delete(msg_id)
        self.assertTrue(deletion_result)

    def test_liking_and_unliking_a_message(self):
        message_result = self.yammer.messages.all()
        msg_id = message_result["messages"][0]["id"]

        like_result = self.yammer.messages.like(msg_id)
        self.assertTrue(like_result)

        unlike_result = self.yammer.messages.unlike(msg_id)
        self.assertTrue(unlike_result)
