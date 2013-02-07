from mock import Mock
from unittest import TestCase

from yampy.apis import MessagesAPI
from yampy.errors import InvalidOpenGraphObjectError, TooManyTopicsError


class MessagesAPIMessageListFetchingTest(TestCase):
    """
    Tests all MessagesAPI methods associated with fetching lists of messages.
    """

    def setUp(self):
        self.mock_get_response = Mock()
        self.mock_client = Mock()
        self.mock_client.get.return_value = self.mock_get_response
        self.messages_api = MessagesAPI(client=self.mock_client)

    def test_all(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.all(**kwargs)

            self.mock_client.get.assert_called_with("/messages", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_from_my_feed(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.from_my_feed(**kwargs)

            self.mock_client.get.assert_called_with("/messages/my_feed", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_from_top_conversations(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.from_top_conversations(**kwargs)

            self.mock_client.get.assert_called_with("/messages/algo", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_from_followed_conversations(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.from_followed_conversations(**kwargs)

            self.mock_client.get.assert_called_with("/messages/following", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_sent(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.sent(**kwargs)

            self.mock_client.get.assert_called_with("/messages/sent", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_private(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.private(**kwargs)

            self.mock_client.get.assert_called_with("/messages/private", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_received(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.received(**kwargs)

            self.mock_client.get.assert_called_with("/messages/received", **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    def test_in_thread(self):
        for kwargs in self.valid_message_list_arguments:
            messages = self.messages_api.in_thread(12345, **kwargs)

            self.mock_client.get.assert_called_with("/messages/in_thread/12345",
                                                    **kwargs)
            self.assertEquals(self.mock_get_response, messages)

    @property
    def valid_message_list_arguments(self):
        return (
            {},
            {"older_than": 12345},
            {"newer_than": 54321},
            {"limit": 30},
            {"threaded": "true"},
            {"threaded": "extended"},
        )


class MessagesAPICreateTest(TestCase):
    def setUp(self):
        self.mock_post_response = Mock()
        self.mock_client = Mock()
        self.mock_client.post.return_value = self.mock_post_response
        self.messages_api = MessagesAPI(client=self.mock_client)

    def test_create_simple_message(self):
        response = self.messages_api.create(body="Hello world")

        self.mock_client.post.assert_called_once_with(
            "/messages",
            body="Hello world",
        )
        self.assertEquals(self.mock_post_response, response)

    def test_create_complex_message(self):
        response = self.messages_api.create(
            body="Hi there",
            group_id=123,
            replied_to_id=456,
            direct_to_id=789,
        )

        self.mock_client.post.assert_called_once_with(
            "/messages",
            body="Hi there",
            group_id=123,
            replied_to_id=456,
            direct_to_id=789,
        )

    def test_create_message_with_topics(self):
        response = self.messages_api.create(
            body="Hi there",
            topics=["unit testing", "yampy"],
        )

        self.mock_client.post.assert_called_once_with(
            "/messages",
            body="Hi there",
            topic1="unit testing",
            topic2="yampy",
        )

    def test_create_message_with_too_many_topics(self):
        with self.assertRaises(TooManyTopicsError):
            self.messages_api.create(
                body="This message has 21 topics",
                topics=["topic %d" % i for i in xrange(21)],
            )

    def test_create_broadcast_message(self):
        response = self.messages_api.create(
            body="This is a public service announcement",
            broadcast=True,
        )

        self.mock_client.post.assert_called_once_with(
            "/messages",
            body="This is a public service announcement",
            broadcast="true",
        )

    def test_create_message_with_an_open_graph_object(self):
        response = self.messages_api.create(
            body="Google is a search engine",
            open_graph_object={
                "url": "http://www.google.com",
                "fetch": True,
            },
        )

        self.mock_client.post.assert_called_once_with(
            "/messages",
            body="Google is a search engine",
            og_url="http://www.google.com",
            og_fetch="true",
        )

    def test_create_message_with_an_invalid_open_graph_object(self):
        with self.assertRaises(InvalidOpenGraphObjectError):
            self.messages_api.create(
                body="Open graph this!",
                open_graph_object={
                    "fetch": True,
                },
            )


class MessagesAPIDeleteTest(TestCase):
    def setUp(self):
        self.mock_delete_response = Mock()
        self.mock_client = Mock()
        self.mock_client.delete.return_value = self.mock_delete_response
        self.messages_api = MessagesAPI(client=self.mock_client)

    def test_delete(self):
        response = self.messages_api.delete(3)

        self.mock_client.delete.assert_called_once_with("/messages/3")
        self.assertEquals(self.mock_delete_response, response)


class MessagesAPILikeTest(TestCase):
    def setUp(self):
        self.mock_post_response = Mock()
        self.mock_delete_response = Mock()
        self.mock_client = Mock()
        self.mock_client.post.return_value = self.mock_post_response
        self.mock_client.delete.return_value = self.mock_delete_response
        self.messages_api = MessagesAPI(client=self.mock_client)

    def test_like(self):
        response = self.messages_api.like(42)

        self.mock_client.post.assert_called_once_with(
            "/messages/liked_by/current",
            message_id=42,
        )
        self.assertEquals(self.mock_post_response, response)

    def test_unlike(self):
        response = self.messages_api.unlike(42)

        self.mock_client.delete.assert_called_once_with(
            "/messages/liked_by/current",
            message_id=42,
        )
        self.assertEquals(self.mock_delete_response, response)
