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
from yampy.apis.utils import ArgumentConverter, IDExtractor, flatten_lists, \
                             flatten_dicts, stringify_booleans, none_filter
from yampy.models import extract_id


def merge_messages(messages, more_messages):
    if messages is None:
        return more_messages
    m = more_messages
    m['messages'] = m['messages'] + messages['messages']
    m['references'] = m['references'] + messages['references']
    return m


class MessagesAPI(object):
    """
    Provides an interface for accessing the message related endpoints of the
    Yammer API. You should not instantiate this class directly; use the
    :meth:`yampy.Yammer.messages` method instead.
    """

    def __init__(self, client):
        """
        Initializes a new MessagesAPI that will use the given ``client`` object
        to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter(
            IDExtractor(r"^(older|newer)_than|.*_id$"),
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

        * ``older_than`` -- Only fetch messages older than this message ID.
        * ``newer_than`` -- Only fetch messages newer than this message ID.
        * ``limit`` -- Only fetch this many messages.
        * ``threaded`` -- Set to ``True`` to only receive the first message of
          each thread, or to ``"extended"`` to recieve the first and two newest
          messages from each thread.
        """
        return self._get_paged_messages("/messages",
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def from_my_feed(self, older_than=None, newer_than=None,
                     limit=None, threaded=None):
        """
        Returns messages from the current user's feed. This will either
        correspond to :meth:`from_top_conversations` or
        :meth:`from_followed_conversations` depending on the user's settings.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        return self._get_paged_messages("/messages/my_feed",
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def from_top_conversations(self, older_than=None, newer_than=None,
                               limit=None, threaded=None):
        """
        Returns messages from the current user's top conversations.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        return self._get_paged_messages("/messages/algo",
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def from_followed_conversations(self, older_than=None, newer_than=None,
                                    limit=None, threaded=None):
        """
        Returns messages from users the current user follows, or groups
        the current user belongs to.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        return self._get_paged_messages("/messages/following",
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def from_group(self, group_id, older_than=None, newer_than=None,
                   limit=None, threaded=None):
        """
        Returns messages from specific group, specified with `group_id`.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        path = "/messages/in_group/%d" % extract_id(group_id)
        return self._get_paged_messages(path, older_than, newer_than,
                                        limit, threaded)

    def sent(self, older_than=None, newer_than=None,
             limit=None, threaded=None):
        """
        Returns of the current user's sent messages.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        return self._get_paged_messages("/messages/sent",
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def private(self, older_than=None, newer_than=None,
                limit=None, threaded=None):
        """
        Returns of the private messages received by the current user.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        return self._get_paged_messages("/messages/private",
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def received(self, older_than=None, newer_than=None,
                 limit=None, threaded=None):
        """
        Returns messages received by the current user.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        return self._get_paged_messages("/messages/received",
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def in_thread(self, thread_id, older_than=None, newer_than=None,
                  limit=None, threaded=None):
        """
        Returns messages that belong to the thread identified by thread_id.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        path = "/messages/in_thread/%d" % extract_id(thread_id)
        return self._get_paged_messages(path,
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def from_user(self, user_id, older_than=None, newer_than=None,
                  limit=None, threaded=None):
        """
        Returns messages that were posted by the user identified by user_id.

        See the :meth:`all` method for a description of the keyword arguments.
        """
        path = "/messages/from_user/%d" % extract_id(user_id)
        return self._get_paged_messages(path,
                                        older_than,
                                        newer_than,
                                        limit, threaded)

    def about_topic(self, topic_id):
        """
        Returns the messages about a topic
        """
        path = "/messages/about_topic/%d" % extract_id(topic_id)
        return self._get_paged_messages(path,
                                        older_than=None,
                                        newer_than=None,
                                        limit=None, threaded=None)

    def find(self, message_id):
        """
        Returns the message identified by the given message_id.
        """
        path = "/messages/%d" % extract_id(message_id)
        return self._get_paged_messages(path,
                                        older_than=None,
                                        newer_than=None,
                                        limit=None, threaded=None)

    def create(self, body, group_id=None, replied_to_id=None,
               direct_to_id=None, topics=[], broadcast=None,
               open_graph_object={}, files=None):
        """
        Posts a new message to Yammer. Returns the new message in the same
        format as the various message listing methods (:meth:`all`,
        :meth:`sent`, etc.).

        The following keyword arguments are supported:

        * ``group_id`` -- Send this message to the group identified by group_id.
        * ``replied_to_id`` -- This message is a reply to the message
          identified by replied_to_id.
        * ``direct_to_id`` -- Send this as a direct message to the user
          identified by direct_to_id.
        * ``topics`` -- A list of topics for the message. Topics should be
          given as strings. There cannot be more than 20 topics for one message.
        * ``broadcast`` -- Set this to True to send a broadcast message. Only
          network admins have permission to send broadcast messages.
        * ``open_graph_object`` -- A dict describing an open graph object to
          attach to the message. It supports the following keys:
           * ``url`` (*required*)
           * ``title``
           * ``image``
           * ``description``
           * ``object_type``
           * ``site_name``
           * ``fetch`` (set to ``True`` to derive other OG data from the URL)
           * ``meta`` (for custom structured data)
        * ``files`` -- A dict containing files to attach to the message.
          the keys shold be ``attachment1`` to ``attachment20``.  The values
          should be open file objects
        """
        if len(topics) > 20:
            raise TooManyTopicsError("Too many topics, the maximum is 20")

        if len(open_graph_object) > 0 and "url" not in open_graph_object:
            raise InvalidOpenGraphObjectError("URL is required")

        return self._client.post("/messages", files=files,
            **self._argument_converter(
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
        return self._client.delete("/messages/%d" % extract_id(message_id))

    def like(self, message_id):
        """
        The current user likes the message identified by message_id.
        """
        return self._client.post(
            "/messages/liked_by/current",
            **self._argument_converter(
                message_id=message_id,
            )
        )

    def unlike(self, message_id):
        """
        Removes the current user's "like" from the message identified by
        message_id.
        """
        return self._client.delete(
            "/messages/liked_by/current",
            **self._argument_converter(
                message_id=message_id,
            )
        )

    def email(self, message_id):
        """
        Emails the message identified by message_id to the authenticated user.
        """
        return self._client.post("/messages/email", **self._argument_converter(
            message_id=message_id,
        ))

    def _get_paged_messages(self, path, older_than=None, newer_than=None,
                            limit=None, threaded=None):
        """
        The message APIs are all the same, in that they return in the meta
        'older_available', i.e. more pages to come.
        This method will page out all historical data.
        """
        def _iter_messages(path, older_than=None, newer_than=None,
                   limit=None, threaded=None):
            messages = self._client.get(path, **self._argument_converter(
                older_than=older_than,
                newer_than=newer_than,
                limit=limit,
                threaded=threaded,
            ))
            try:
                older_available = messages['meta']['older_available']
            except KeyError:
                older_available = False
            return (older_available,
                    messages,
                    messages['messages'][-1:][0]['id'])
        are_more = True
        messages = None
        while are_more:
            are_more, more_messages, last_message = _iter_messages(
                path,
                older_than,
                newer_than,
                limit,
                threaded)
            older_than = last_message
            messages = merge_messages(messages, more_messages)
        return messages
