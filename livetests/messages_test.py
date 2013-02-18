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
Tests for posting and reading messages.
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
