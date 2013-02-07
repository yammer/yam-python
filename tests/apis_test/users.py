from mock import Mock
from unittest import TestCase

from yampy.apis import UsersAPI


class UsersAPIAllTest(TestCase):
    def setUp(self):
        self.mock_get_response = Mock()
        self.mock_client = Mock()
        self.mock_client.get.return_value = self.mock_get_response
        self.users_api = UsersAPI(client=self.mock_client)

    def test_all(self):
        users = self.users_api.all()

        self.mock_client.get.assert_called_once_with("/users")
        self.assertEquals(self.mock_get_response, users)

    def test_all_with_pagination(self):
        users = self.users_api.all(page=2)

        self.mock_client.get.assert_called_once_with("/users", page=2)
        self.assertEquals(self.mock_get_response, users)

    def test_all_with_first_letter_of_username(self):
        users = self.users_api.all(letter="g")

        self.mock_client.get.assert_called_once_with("/users", letter="g")
        self.assertEquals(self.mock_get_response, users)

    def test_all_with_custom_sorting(self):
        users = self.users_api.all(sort_by="followers", reverse=True)

        self.mock_client.get.assert_called_once_with(
            "/users",
            sort_by="followers",
            reverse="true",
        )
        self.assertEquals(self.mock_get_response, users)
