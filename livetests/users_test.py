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
Tests for getting and updating users.
"""

from unittest import TestCase

from support import skip_without_environment_variable
import yampy


class UsersIntegrationTest(TestCase):
    @skip_without_environment_variable("YAMMER_ACCESS_TOKEN")
    def test_reading_and_updating_current_user(self, access_token):
        yammer = yampy.Yammer(access_token)

        current_user = yammer.users.find_current()
        self.assertIn("id", current_user)
        self.assertIn("full_name", current_user)

        user_id = current_user.id
        original_full_name = current_user.full_name

        result = yammer.users.update(user_id, full_name="Just Testing")
        self.assertTrue(result)

        updated_user = yammer.users.find_current()
        self.assertIn("full_name", updated_user)
        self.assertEqual("Just Testing", updated_user.full_name)

        result = yammer.users.update(user_id, full_name=original_full_name)
        self.assertTrue(result)
