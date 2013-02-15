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

from yampy.errors import InvalidOpenGraphObjectError, TooManyTopicsError
from yampy.apis.utils import ArgumentConverter, flatten_lists, flatten_dicts, \
                             stringify_booleans, none_filter


class MessagesAPI(object):
    """
    Provides an interface for accessing the message related endpoints of the
    Yammer API.
    """

    def __init__(self, client):
        """
        Initializes a new MessagesAPI that will use the given client object
        to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter(
            flatten_lists,
            flatten_dicts,
            stringify_booleans,
            none_filter,
        )

    def all(self, older_than=None, newer_than=None,
            limit=None, threaded=None):
        """
        Returns public messages from the current user's network.

        Customize the response using the keyword arguments:
        older_than -- Only fetch messages older than this message ID.
        newer_than -- Only fetch messages newer than this message ID.
        limit -- Only fetch this many messages.
        threaded -- Set to "true" to only receive the first message of each
            thread, or to "extended" to recieve the first and two newest
            messages from each thread.
        """
        return self._client.get("/messages", **self._argument_converter(
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        ))

    def from_my_feed(self, older_than=None, newer_than=None,
                     limit=None, threaded=None):
        """
        Returns messages from the current user's feed. This will either
        correspond to from_top_conversations or from_followed_conversations
        depending on the user's settings.

        See the "all" method for a description of the keyword arguments.
        """
        return self._client.get("/messages/my_feed", **self._argument_converter(
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        ))

    def from_top_conversations(self, older_than=None, newer_than=None,
                               limit=None, threaded=None):
        """
        Returns messages from the current user's top conversations.

        See the "all" method for a description of the keyword arguments.
        """
        return self._client.get("/messages/algo", **self._argument_converter(
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        ))

    def from_followed_conversations(self, older_than=None, newer_than=None,
                                    limit=None, threaded=None):
        """
        Returns messages from users the current user follows, or groups
        the current user belongs to.

        See the "all" method for a description of the keyword arguments.
        """
        return self._client.get("/messages/following", **self._argument_converter(
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        ))

    def sent(self, older_than=None, newer_than=None,
             limit=None, threaded=None):
        """
        Returns of the current user's sent messages.

        See the "all" method for a description of the keyword arguments.
        """
        return self._client.get("/messages/sent", **self._argument_converter(
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        ))

    def private(self, older_than=None, newer_than=None,
                limit=None, threaded=None):
        """
        Returns of the private messages received by the current user.

        See the "all" method for a description of the keyword arguments.
        """
        return self._client.get("/messages/private", **self._argument_converter(
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        ))

    def received(self, older_than=None, newer_than=None,
                 limit=None, threaded=None):
        """
        Returns messages received by the current user.

        See the "all" method for a description of the keyword arguments.
        """
        return self._client.get("/messages/received", **self._argument_converter(
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        ))

    def in_thread(self, thread_id, older_than=None, newer_than=None,
                  limit=None, threaded=None):
        """
        Returns messages that belong to the thread identified by thread_id.

        See the "all" method for a description of the keyword arguments.
        """
        path = "/messages/in_thread/%d" % thread_id
        return self._client.get(path, **self._argument_converter(
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        ))

    def create(self, body, group_id=None, replied_to_id=None,
               direct_to_id=None, topics=[], broadcast=None,
               open_graph_object={}):
        """
        Posts a new message to Yammer. Returns the new message in the same
        format as the various message listing methods ("all", "sent", etc.).
        """
        if len(topics) > 20:
            raise TooManyTopicsError("Too many topics, the maximum is 20")

        if len(open_graph_object) > 0 and "url" not in open_graph_object:
            raise InvalidOpenGraphObjectError("URL is required")

        return self._client.post("/messages", **self._argument_converter(
            body=body,
            group_id=group_id,
            replied_to_id=replied_to_id,
            direct_to_id=direct_to_id,
            topic=topics,
            broadcast=broadcast,
            og=open_graph_object,
        ))

    def delete(self, message_id):
        """
        Deletes the message identified by message_id.
        """
        return self._client.delete("/messages/%d" % message_id)

    def like(self, message_id):
        """
        The current user likes the message identified by message_id.
        """
        return self._client.post(
            "/messages/liked_by/current",
            message_id=message_id,
        )

    def unlike(self, message_id):
        """
        Removes the current user's "like" from the message identified by
        message_id.
        """
        return self._client.delete(
            "/messages/liked_by/current",
            message_id=message_id,
        )
