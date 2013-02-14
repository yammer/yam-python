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

from unittest import TestCase
from mock import patch, Mock

from yampy import Yammer
from yampy.client import Client
from yampy.apis import MessagesAPI, UsersAPI

class YammerTest(TestCase):
    @patch("yampy.yammer.MessagesAPI", spec=True)
    @patch("yampy.yammer.Client", spec=True)
    def test_messages_returns_a_messages_api_instance(self, MockClient,
                                                      MockMessagesAPI):
        yammer = Yammer(access_token="abc123")
        messages = yammer.messages

        MockClient.assert_called_once_with(
            access_token="abc123",
            base_url=None,
        )
        MockMessagesAPI.assert_called_once_with(
            client=MockClient(),
        )
        self.assertIsInstance(messages, MessagesAPI)

    @patch("yampy.yammer.UsersAPI", spec=True)
    @patch("yampy.yammer.Client", spec=True)
    def test_users_returns_a_users_api_instance(self, MockClient,
                                                MockUsersAPI):
        yammer = Yammer(access_token="abc123")
        users = yammer.users

        MockClient.assert_called_once_with(
            access_token="abc123",
            base_url=None,
        )
        MockUsersAPI.assert_called_once_with(
            client=MockClient(),
        )
        self.assertIsInstance(users, UsersAPI)

    @patch("yampy.yammer.Client", spec=True)
    def test_client_returns_a_client_instance(self, MockClient):
        yammer = Yammer(access_token="thx1138")
        client = yammer.client

        MockClient.assert_called_once_with(
            access_token="thx1138",
            base_url=None,
        )
        self.assertIsInstance(client, Client)
