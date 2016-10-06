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

from .apis import MessagesAPI, TopicsAPI, UsersAPI, GroupsAPI
from .client import Client


class Yammer(object):

    """
    Main entry point for accessing the Yammer API.

    Essentially this is just a Factory class that provides instances of various
    classes that interact directly with the API. For example, the ``messages``
    method returns a ``MessagesAPI`` object.
    """

    def __init__(self, access_token=None, base_url=None):
        """
        Initialize a new Yammer instance.

        * ``access_token`` identifies the current user. You can acquire an
          access token using an :class:`yampy.Authenticator`.
        * ``base_url`` defaults to the live Yammer API. Provide a different
          base URL to make requests against some other server, e.g. a fake
          in your application's test suite.
        """
        self._client = Client(access_token=access_token, base_url=base_url)

    @property
    def client(self):
        """
        Returns a :class:`yampy.client.Client` object which can be used to make
        HTTP requests to any of the Yammer REST API endpoints.

        You should use this if there isn't a more specific interface available
        for the request you want to make, e.g. if you want to request users you
        should use the ``users`` method instead of the ``client`` method.
        """
        return self._client

    @property
    def messages(self):
        """
        Returns a :class:`yampy.apis.MessagesAPI` object which can be used to
        call the Yammer API's message-related endpoints.
        """
        if not hasattr(self, "_messages_api"):
            self._messages_api = MessagesAPI(client=self._client)
        return self._messages_api

    @property
    def topics(self):
        """
        Returns a :class:`yampy.apis.TopicsAPI` object which can be used to
        call the Yammer API's topic-related endpoints.
        """
        if not hasattr(self, "_topics_api"):
            self._topics_api = TopicsAPI(client=self._client)
        return self._topics_api

    @property
    def users(self):
        """
        Returns a :class:`yampy.apis.UsersAPI` object which can be used to call
        the Yammer API's user-related endpoints.
        """
        if not hasattr(self, "_users_api"):
            self._users_api = UsersAPI(client=self._client)
        return self._users_api

    @property
    def groups(self):
        """
        Returns a :class:`yampy.apis.GroupsAPI` object which can be used to call
        the Yammer API's user-related endpoints.
        """
        if not hasattr(self, "_groups_api"):
            self._groups_api = GroupsAPI(client=self._client)
        return self._groups_api
