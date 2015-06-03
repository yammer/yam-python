"""
Tests for getting groups.
"""

from unittest import TestCase

from livetests.support import skip_without_environment_variable
import yampy


class GroupsIntegrationTest(TestCase):

    @skip_without_environment_variable("YAMMER_ACCESS_TOKEN")
    def test_reading_and_updating_current_user(self, access_token):
        yammer = yampy.Yammer(access_token)
        test_group_name = 'Test Group'
        cur_user = yammer.users.find_current()

        new_group = yammer.groups.create(test_group_name)
        self.assertIn("creator_id", new_group)
        self.assertIn("full_name", new_group)
        self.assertEqual(new_group.full_name, test_group_name)
        self.assertEqual(new_group.creator_id, cur_user.id)

        result = yammer.groups.delete(new_group)
        self.assertTrue(result)
