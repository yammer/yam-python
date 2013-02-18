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
Tests for interacting with messages.
"""

from datetime import datetime
from unittest import TestCase

from livetests.support import skip_without_environment_variable
import yampy


class MessagesIntegrationTest(TestCase):
    @skip_without_environment_variable("YAMMER_ACCESS_TOKEN")
    def test_posting_reading_and_deleting_messages(self, access_token):
        yammer = yampy.Yammer(access_token)
        test_message = "The time is %s" % datetime.now()

        result = yammer.messages.create(body=test_message)
        new_message = result.messages[0]
        self.assertEqual(new_message.body.plain, test_message)

        all_messages = yammer.messages.all()
        self.assertIn(test_message, str(all_messages))

        yammer.messages.delete(new_message.id)

        all_messages = yammer.messages.all()
        self.assertNotIn(test_message, str(all_messages))

    @skip_without_environment_variable("YAMMER_ACCESS_TOKEN")
    def test_liking_and_unliking_messages(self, access_token):
        yammer = yampy.Yammer(access_token)
        message = self.message_not_liked_by_current_user(yammer)
        me = yammer.users.find_current()

        yammer.messages.like(message)
        reloaded_message = yammer.messages.find(message)

        self.assert_user_likes_message(me, reloaded_message)

        yammer.messages.unlike(message)
        reloaded_message = yammer.messages.find(message)

        self.assert_user_does_not_like_message(me, reloaded_message)

    def message_not_liked_by_current_user(self, yammer):
        all_messages = yammer.messages.all().messages
        me = yammer.users.find_current()
        for message in all_messages:
            liker_ids = self._user_ids_liking_message(message)
            if me.id not in liker_ids:
                return message
        self.fail("The current user has liked all available messages")

    def assert_user_likes_message(self, user, message):
        liker_ids = self._user_ids_liking_message(message)
        self.assertIn(user.id, liker_ids)

    def assert_user_does_not_like_message(self, user, message):
        liker_ids = self._user_ids_liking_message(message)
        self.assertNotIn(user.id, liker_ids)

    def _user_ids_liking_message(self, message):
        return set([like.user_id for like in message.liked_by.names])
