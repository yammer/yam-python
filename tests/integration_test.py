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

"""
Tests for excercising the whole system in concert.
"""

from .support.integration import TestCaseWithFakeYammerServer
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

        self.assertEqual(3, len(message_result.messages))

    def test_creating_a_message(self):
        message_result = self.yammer.messages.create(
            body="Hello everyone!",
            topics=["python", "testing"],
            group_id=345,
        )

        self.assertEqual(1, len(message_result.messages))
        message = message_result.messages[0]

        self.assertEqual("Hello everyone!", message.body.plain)

    def test_deleting_a_message(self):
        message_result = self.yammer.messages.all()
        msg_id = message_result.messages[0].id

        deletion_result = self.yammer.messages.delete(msg_id)
        self.assertTrue(deletion_result)

    def test_liking_and_unliking_a_message(self):
        message_result = self.yammer.messages.all()
        msg_id = message_result.messages[0].id

        like_result = self.yammer.messages.like(msg_id)
        self.assertTrue(like_result)

        unlike_result = self.yammer.messages.unlike(msg_id)
        self.assertTrue(unlike_result)


class UserIntegrationTest(TestCaseWithFakeYammerServer):
    def setUp(self):
        super(UserIntegrationTest, self).setUp()
        self.yammer = yampy.Yammer(
            access_token="valid_token",
            base_url="http://localhost:5000/api/v1",
        )

    def test_fetching_users(self):
        users = self.yammer.users.all()
        self.assertEqual(3, len(users))

    def test_fetching_individual_users(self):
        current_user = self.yammer.users.find_current()
        self.assertEqual("Joe Bloggs", current_user.full_name)

        user_by_id = self.yammer.users.find(13)
        self.assertEqual(13, user_by_id.id)

    def test_creating_a_user(self):
        user_result = self.yammer.users.create(
            email_address="john.doe@example.com",
            full_name="John Doe",
            education=[
                {
                    "school": "Manchester University",
                    "degree": "BSc",
                    "description": "Computer Science",
                    "start_year": "2002",
                    "end_year": "2005",
                },
            ],
        )

    def test_updating_a_user(self):
        update_result = self.yammer.users.update(
            user_id=1,
            full_name="John Smith",
        )
        self.assertTrue(update_result)

    def test_suspending_a_user(self):
        suspend_result = self.yammer.users.suspend(123)
        self.assertTrue(suspend_result)

    def test_deleting_a_user(self):
        delete_result = self.yammer.users.delete(123)
        self.assertTrue(delete_result)
