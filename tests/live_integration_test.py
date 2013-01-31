"""
Tests integration with the live Yammer API. These tests require a
YAMMER_ACCESS_TOKEN environment variable to run. Please note that they will
post real messages, so don't authenticate an account you really care about.
"""

from datetime import datetime
from unittest import TestCase

from support import skip_without_environment_variable

import yampy


class MessagesIntegrationTest(TestCase):
    @skip_without_environment_variable("YAMMER_ACCESS_TOKEN")
    def test_posting_and_reading_a_message(self, access_token):
        yammer = yampy.Client(access_token)
        test_message = "The time is %s" % datetime.now()

        result = yammer.post("/messages", body=test_message)

        self.assertIn("messages", result)
        message = result["messages"][0]
        self.assertEqual(message["body"]["plain"], test_message)

        all_messages = yammer.get("/messages")
        self.assertIn(test_message, str(all_messages))
