from mock import Mock

from tests.support.unit import TestCaseWithMockClient
from yampy.apis import GroupsAPI


class GroupsAPIAllTest(TestCaseWithMockClient):

    def setUp(self):
        super(GroupsAPIAllTest, self).setUp()
        self.groups_api = GroupsAPI(client=self.mock_client)

    def test_all(self):
        groups = self.groups_api.all()

        self.mock_client.get.assert_called_once_with("/groups")
        self.assertEquals(self.mock_get_response, groups)

    def test_all_with_reverse(self):
        groups = self.groups_api.all(reverse=True)

        self.mock_client.get.assert_called_once_with(
            "/groups",
            reverse="true",
        )
        self.assertEquals(self.mock_get_response, groups)

    def test_find_current(self):
        current_user_groups = self.groups_api.all(mine=True)

        self.mock_client.get.assert_called_once_with("/groups", mine="true")
        self.assertEquals(self.mock_get_response, current_user_groups)


class GroupsAPIFindTest(TestCaseWithMockClient):

    def setUp(self):
        super(GroupsAPIFindTest, self).setUp()
        self.groups_api = GroupsAPI(client=self.mock_client)

    def test_find(self):
        found_group = self.groups_api.find(13)

        self.mock_client.get.assert_called_once_with("/groups/13")
        self.assertEquals(self.mock_get_response, found_group)

    def test_find_passing_id_as_a_dict(self):
        found_group = self.groups_api.find({"id": 31})

        self.mock_client.get.assert_called_once_with("/groups/31")
        self.assertEquals(self.mock_get_response, found_group)

    def test_find_passing_id_as_an_object(self):
        found_group = self.groups_api.find(Mock(id=27))

        self.mock_client.get.assert_called_once_with("/groups/27")
        self.assertEquals(self.mock_get_response, found_group)


class GroupsUsersAPICreateTest(TestCaseWithMockClient):

    def setUp(self):
        super(GroupsUsersAPICreateTest, self).setUp()
        self.groups_api = GroupsAPI(client=self.mock_client)

    def test_create_public_group(self):
        created_group = self.groups_api.create("Test Public group")

        self.mock_client.post.assert_called_once_with(
            "/groups",
            name="Test Public group",
            private="false",
        )
        self.assertEquals(self.mock_post_response, created_group)

    def test_create_private_group(self):
        created_group = self.groups_api.create(
            "Test Private group", private=True)

        self.mock_client.post.assert_called_once_with(
            "/groups",
            name="Test Private group",
            private="true",
        )
        self.assertEquals(self.mock_post_response, created_group)


class GroupsAPIDeleteTest(TestCaseWithMockClient):

    def setUp(self):
        super(GroupsAPIDeleteTest, self).setUp()
        self.groups_api = GroupsAPI(client=self.mock_client)

    def test_delete(self):
        delete_result = self.groups_api.delete(123)

        self.mock_client.delete.assert_called_once_with(
            "/groups/123",
            delete="true",
        )
        self.assertEquals(self.mock_delete_response, delete_result)

    def test_delete_passing_id_as_a_dict(self):
        delete_result = self.groups_api.delete({"id": 171})

        self.mock_client.delete.assert_called_once_with(
            "/groups/171",
            delete="true",
        )
        self.assertEquals(self.mock_delete_response, delete_result)

    def test_delete_passing_id_as_an_object(self):
        delete_result = self.groups_api.delete(Mock(id=125))

        self.mock_client.delete.assert_called_once_with(
            "/groups/125",
            delete="true",
        )
        self.assertEquals(self.mock_delete_response, delete_result)


class GroupsAPIJoinTest(TestCaseWithMockClient):

    def setUp(self):
        super(GroupsAPIJoinTest, self).setUp()
        self.groups_api = GroupsAPI(client=self.mock_client)

    def test_join(self):
        response = self.groups_api.join(171)

        self.mock_client.post.assert_called_once_with(
            "/group_memberships",
            group_id=171,
        )
        self.assertEquals(self.mock_post_response, response)

    def test_join_passing_id_as_a_dict(self):
        response = self.groups_api.join({"id": 171})

        self.mock_client.post.assert_called_once_with(
            "/group_memberships",
            group_id=171,
        )
        self.assertEquals(self.mock_post_response, response)

    def test_join_passing_id_as_an_object(self):
        response = self.groups_api.join(Mock(id=125))

        self.mock_client.post.assert_called_once_with(
            "/group_memberships",
            group_id=125,
        )
        self.assertEquals(self.mock_post_response, response)


class GroupsAPILeaveTest(TestCaseWithMockClient):

    def setUp(self):
        super(GroupsAPILeaveTest, self).setUp()
        self.groups_api = GroupsAPI(client=self.mock_client)

    def test_leave(self):
        self.groups_api.leave(142)

        self.mock_client.delete.assert_called_once_with(
            "/group_memberships",
            group_id=142,
        )

    def test_leave_passing_id_as_a_dict(self):
        self.groups_api.leave({"id": 171})

        self.mock_client.delete.assert_called_once_with(
            "/group_memberships",
            group_id=171,
        )

    def test_leave_passing_id_as_an_object(self):
        self.groups_api.leave(Mock(id=125))

        self.mock_client.delete.assert_called_once_with(
            "/group_memberships",
            group_id=125,
        )
