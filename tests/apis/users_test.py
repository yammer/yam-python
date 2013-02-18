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

from mock import Mock

from tests.support.unit import TestCaseWithMockClient
from yampy.apis import UsersAPI
from yampy.errors import InvalidEducationRecordError, \
                         InvalidPreviousCompanyRecord


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

    def test_in_group_passing_id_as_a_dict(self):
        self.users_api.in_group({"id": 14})

        self.mock_client.get.assert_called_once_with("/users/in_group/14")

    def test_in_group_passing_id_as_an_object(self):
        self.users_api.in_group(Mock(id=44))

        self.mock_client.get.assert_called_once_with("/users/in_group/44")

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

    def test_find_current_with_additional_information(self):
        current_user = self.users_api.find_current(
            include_followed_users=True,
            include_followed_tags=True,
            include_group_memberships=True,
        )

        self.mock_client.get.assert_called_once_with(
            "/users/current",
            include_followed_users="true",
            include_followed_tags="true",
            include_group_memberships="true",
        )
        self.assertEquals(self.mock_get_response, current_user)

    def test_find(self):
        found_user = self.users_api.find(13)

        self.mock_client.get.assert_called_once_with("/users/13")
        self.assertEquals(self.mock_get_response, found_user)

    def test_find_passing_id_as_a_dict(self):
        self.users_api.find({"id": 31})

        self.mock_client.get.assert_called_once_with("/users/31")

    def test_find_passing_id_as_an_object(self):
        self.users_api.find(Mock(id=27))

        self.mock_client.get.assert_called_once_with("/users/27")

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

    def test_create_user_with_a_single_education_record(self):
        self.users_api.create(
            email_address="person@example.org",
            education={
                "school": "MIT",
                "degree": "MSc",
                "description": "Architecture",
                "start_year": "2001",
                "end_year": "2005",
            },
        )

        self.mock_client.post.assert_called_once_with(
            "/users",
            email="person@example.org",
            education=[
                "MIT,MSc,Architecture,2001,2005",
            ]
        )

    def test_create_user_with_employment_history(self):
        created_user = self.users_api.create(
            email_address="ripley@example.org",
            previous_companies=(
                {
                    "company": "Acme Inc.",
                    "position": "developer",
                    "description": "writing code",
                    "start_year": "2001",
                    "end_year": "2012",
                },
                {
                    "company": "Weyland Yutani",
                    "position": "terraforming engineer",
                    "description": "fighting aliens",
                    "start_year": "2110",
                    "end_year": "2119",
                }
            ),
        )

        self.mock_client.post.assert_called_once_with(
            "/users",
            email="ripley@example.org",
            previous_companies=[
                "Acme Inc.,developer,writing code,2001,2012",
                "Weyland Yutani,terraforming engineer,fighting aliens,2110,2119",
            ],
        )

    def test_create_user_with_invalid_employment_history(self):
        with self.assertRaises(InvalidPreviousCompanyRecord):
            self.users_api.create(
                email_address="someone@example.com",
                previous_companies=[
                    {
                        "company": "Incomplete",
                    }
                ],
            )

    def test_create_user_with_a_single_employment_history_record(self):
        self.users_api.create(
            email_address="someone@example.com",
            previous_companies={
                "company": "Blue Sun",
                "position": "T-shirt printer",
                "description": "Making t-shirts",
                "start_year": "2515",
                "end_year": "2517",
            },
        )

        self.mock_client.post.assert_called_once_with(
            "/users",
            email="someone@example.com",
            previous_companies=[
                "Blue Sun,T-shirt printer,Making t-shirts,2515,2517",
            ],
        )


class UsersAPIUpdateTest(TestCaseWithMockClient):
    def setUp(self):
        super(UsersAPIUpdateTest, self).setUp()
        self.users_api = UsersAPI(client=self.mock_client)

    def test_update_user(self):
        result = self.users_api.update(
            user_id=12345,
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

        self.mock_client.put.assert_called_once_with(
            "/users/12345",
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
        self.assertEquals(self.mock_put_response, result)

    def test_update_user_with_education_history(self):
        self.users_api.update(
            user_id=7,
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

        self.mock_client.put.assert_called_once_with(
            "/users/7",
            education=[
                "Manchester University,BSc,Computer Science,2002,2005",
                "Imperial College,MSc,Computer Science,2005,2006",
            ]
        )

    def test_update_user_with_invalid_education_history(self):
        with self.assertRaises(InvalidEducationRecordError):
            self.users_api.update(
                user_id=12,
                education=(
                    {
                        "description": "Computer Science",
                        "start_year": "2005",
                        "end_year": "2006",
                    },
                ),
            )

    def test_update_user_with_employment_history(self):
        self.users_api.update(
            user_id=123,
            previous_companies=(
                {
                    "company": "Acme Inc.",
                    "position": "developer",
                    "description": "making software",
                    "start_year": "2001",
                    "end_year": "2012",
                },
                {
                    "company": "Weyland Yutani",
                    "position": "terraforming engineer",
                    "description": "mostly dull routine",
                    "start_year": "2110",
                    "end_year": "2119",
                }
            ),
        )

        self.mock_client.put.assert_called_once_with(
            "/users/123",
            previous_companies=[
                "Acme Inc.,developer,making software,2001,2012",
                "Weyland Yutani,terraforming engineer,mostly dull routine,2110,2119",
            ],
        )

    def test_update_user_with_invalid_employment_history(self):
        with self.assertRaises(InvalidPreviousCompanyRecord):
            self.users_api.update(
                user_id=77,
                previous_companies=[
                    {
                        "company": "Incomplete",
                    }
                ],
            )

    def test_update_user_passing_id_as_a_dict(self):
        self.users_api.update(
            user_id={"id": 11},
            full_name="Joe Bloggs",
        )

        self.mock_client.put.assert_called_once_with(
            "/users/11",
            full_name="Joe Bloggs",
        )

    def test_update_user_passing_id_as_an_object(self):
        self.users_api.update(
            user_id=Mock(id=117),
            full_name="Joe Bloggs",
        )

        self.mock_client.put.assert_called_once_with(
            "/users/117",
            full_name="Joe Bloggs",
        )


class UsersAPISuspendAndDeleteTest(TestCaseWithMockClient):
    def setUp(self):
        super(UsersAPISuspendAndDeleteTest, self).setUp()
        self.users_api = UsersAPI(client=self.mock_client)

    def test_suspend(self):
        suspend_result = self.users_api.suspend(123)

        self.mock_client.delete.assert_called_once_with("/users/123")
        self.assertEquals(self.mock_delete_response, suspend_result)

    def test_suspend_passing_id_as_a_dict(self):
        self.users_api.suspend({"id": 17})

        self.mock_client.delete.assert_called_once_with("/users/17")

    def test_suspend_passing_id_as_an_object(self):
        self.users_api.suspend(Mock(id=12))

        self.mock_client.delete.assert_called_once_with("/users/12")

    def test_delete(self):
        delete_result = self.users_api.delete(123)

        self.mock_client.delete.assert_called_once_with(
            "/users/123",
            delete="true",
        )
        self.assertEquals(self.mock_delete_response, delete_result)
