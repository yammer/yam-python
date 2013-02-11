"""
Tests for posting and reading messages.
"""

from datetime import datetime
from unittest import TestCase

from support import skip_without_environment_variable
import yampy


class MessagesIntegrationTest(TestCase):
    @skip_without_environment_variable("YAMMER_ACCESS_TOKEN")
    def test_posting_reading_and_deleting_messages(self, access_token):
        yammer = yampy.Yammer(access_token)
        test_message = "The time is %s" % datetime.now()

        result = yammer.messages.create(body=test_message)
        new_message = result["messages"][0]
        self.assertEqual(new_message["body"]["plain"], test_message)

        all_messages = yammer.messages.all()
        self.assertIn(test_message, str(all_messages))

        yammer.messages.delete(new_message["id"])

        all_messages = yammer.messages.all()
        self.assertNotIn(test_message, str(all_messages))
