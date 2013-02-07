"""
Tests for excercising the whole system in concert.
"""

from support.integration import TestCaseWithFakeYammerServer
import yampy


class MessageIntegrationTest(TestCaseWithFakeYammerServer):
    def test_fetching_messages(self):
        authenticator = yampy.Authenticator(
            client_id="valid_client_id",
            client_secret="valid_client_secret",
            oauth_base_url="http://localhost:5000/oauth2",
        )

        access_token = authenticator.fetch_access_token("valid_code")

        yammer = yampy.Yammer(
            access_token=access_token,
            base_url="http://localhost:5000/api/v1",
        )
        message_result = yammer.messages.all()

        self.assertEqual(3, len(message_result["messages"]))
