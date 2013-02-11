from mock import Mock

from tests.support.unit import TestCaseWithMockClient
from yampy.apis import UsersAPI
from yampy.errors import InvalidEducationRecordError


class UsersAPIAllTest(TestCaseWithMockClient):
    def setUp(self):
        super(UsersAPIAllTest, self).setUp()
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


class UsersAPIInGroupTest(TestCaseWithMockClient):
    def setUp(self):
        super(UsersAPIInGroupTest, self).setUp()
        self.users_api = UsersAPI(client=self.mock_client)

    def test_in_group(self):
        users = self.users_api.in_group(194)

        self.mock_client.get.assert_called_once_with("/users/in_group/194")
        self.assertEquals(self.mock_get_response, users)

    def test_in_group_with_page(self):
        users = self.users_api.in_group(42, page=7)

        self.mock_client.get.assert_called_once_with(
            "/users/in_group/42",
            page=7,
        )
        self.assertEquals(self.mock_get_response, users)


class UsersAPIFindTest(TestCaseWithMockClient):
    def setUp(self):
        super(UsersAPIFindTest, self).setUp()
        self.users_api = UsersAPI(client=self.mock_client)

    def test_find_current(self):
        current_user = self.users_api.find_current()

        self.mock_client.get.assert_called_once_with("/users/current")
        self.assertEquals(self.mock_get_response, current_user)

    def test_find(self):
        found_user = self.users_api.find(13)

        self.mock_client.get.assert_called_once_with("/users/13")
        self.assertEquals(self.mock_get_response, found_user)

    def test_find_by_email(self):
        found_user = self.users_api.find_by_email("user@example.org")

        self.mock_client.get.assert_called_once_with(
            "/users/by_email",
            email="user@example.org",
        )
        self.assertEquals(self.mock_get_response, found_user)


class UsersAPICreateTest(TestCaseWithMockClient):
    def setUp(self):
        super(UsersAPICreateTest, self).setUp()
        self.users_api = UsersAPI(client=self.mock_client)

    def test_create_simple_user(self):
        created_user = self.users_api.create("user@example.com")

        self.mock_client.post.assert_called_once_with(
            "/users",
            email="user@example.com",
        )
        self.assertEquals(self.mock_post_response, created_user)

    def test_create_complex_user(self):
        created_user = self.users_api.create(
            email_address="someone@example.org",
            full_name="John Doe",
            job_title="Developer",
            location="Stockholm, Sweden",
            im={
                "provider": "gtalk",
                "username": "someone@gmail.example.com",
            },
            work_telephone="+46123123123",
            work_extension="123",
            mobile_telephone="+46789789789",
            significant_other="Jane",
            kids_names="Tom, Dick and Harry",
            interests="Programming, testing",
            summary="Zaphod's just this guy, y'know?",
            expertise="Work and stuff",
        )

        self.mock_client.post.assert_called_once_with(
            "/users",
            email="someone@example.org",
            full_name="John Doe",
            job_title="Developer",
            location="Stockholm, Sweden",
            im_provider="gtalk",
            im_username="someone@gmail.example.com",
            work_telephone="+46123123123",
            work_extension="123",
            mobile_telephone="+46789789789",
            significant_other="Jane",
            kids_names="Tom, Dick and Harry",
            interests="Programming, testing",
            summary="Zaphod's just this guy, y'know?",
            expertise="Work and stuff",
        )

    def test_create_user_with_education_history(self):
        created_user = self.users_api.create(
            email_address="person@example.org",
            education=(
                {
                    "school": "Manchester University",
                    "degree": "BSc",
                    "description": "Computer Science",
                    "start_year": "2002",
                    "end_year": "2005",
                },
                {
                    "school": "Imperial College",
                    "degree": "MSc",
                    "description": "Computer Science",
                    "start_year": "2005",
                    "end_year": "2006",
                }
            ),
        )

        self.mock_client.post.assert_called_once_with(
            "/users",
            email="person@example.org",
            education=[
                "Manchester University,BSc,Computer Science,2002,2005",
                "Imperial College,MSc,Computer Science,2005,2006",
            ]
        )

    def test_create_user_with_invalid_education_history(self):
        with self.assertRaises(InvalidEducationRecordError):
            self.users_api.create(
                email_address="person@example.org",
                education=(
                    {
                        "description": "Computer Science",
                        "start_year": "2005",
                        "end_year": "2006",
                    },
                ),
            )
