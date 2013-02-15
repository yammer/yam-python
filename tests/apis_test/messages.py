from mock import Mock

from tests.support.unit import TestCaseWithMockClient
from yampy.apis import MessagesAPI
from yampy.errors import InvalidOpenGraphObjectError, TooManyTopicsError


class MessagesAPIMessageListFetchingTest(TestCaseWithMockClient):
    """
    Tests all MessagesAPI methods associated with fetching lists of messages.
    """

    def setUp(self):
        super(MessagesAPIMessageListFetchingTest, self).setUp()
        self.messages_api = MessagesAPI(client=self.mock_client)

    def test_all(self):
        self._test_list_fetch("/messages", self.messages_api.all)

    def test_from_my_feed(self):
        self._test_list_fetch("/messages/my_feed", self.messages_api.from_my_feed)

    def test_from_top_conversations(self):
        self._test_list_fetch("/messages/algo", self.messages_api.from_top_conversations)

    def test_from_followed_conversations(self):
        self._test_list_fetch("/messages/following", self.messages_api.from_followed_conversations)

    def test_sent(self):
        self._test_list_fetch("/messages/sent", self.messages_api.sent)

    def test_private(self):
        self._test_list_fetch("/messages/private", self.messages_api.private)

    def test_received(self):
        self._test_list_fetch("/messages/received", self.messages_api.received)

    def test_in_thread(self):
        self._test_list_fetch("/messages/in_thread/12345", self.messages_api.in_thread, 12345)

    def test_in_thread_passing_id_as_a_dict(self):
        self._test_list_fetch("/messages/in_thread/321", self.messages_api.in_thread, {"id": 321})

    def test_in_thread_passing_id_as_an_object(self):
        self._test_list_fetch("/messages/in_thread/223", self.messages_api.in_thread, Mock(id=223))

    def _test_list_fetch(self, path, method, *method_args):
        for kwargs in self.valid_message_list_arguments:
            messages = method(*method_args, **kwargs)

            self.mock_client.get.assert_called_with(path, **kwargs)
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


class MessagesAPICreateTest(TestCaseWithMockClient):
    def setUp(self):
        super(MessagesAPICreateTest, self).setUp()
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

    def test_create_passing_ids_as_dicts(self):
        self.messages_api.create(
            body="Hello world",
            group_id={"id": 123},
            replied_to_id={"id": 456},
            direct_to_id={"id": 789},
        )

        self.mock_client.post.assert_called_once_with(
            "/messages",
            body="Hello world",
            group_id=123,
            replied_to_id=456,
            direct_to_id=789,
        )

    def test_create_passing_ids_as_objects(self):
        self.messages_api.create(
            body="Hello world",
            replied_to_id=Mock(id=37),
        )

        self.mock_client.post.assert_called_once_with(
            "/messages",
            body="Hello world",
            replied_to_id=37,
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


class MessagesAPIDeleteTest(TestCaseWithMockClient):
    def setUp(self):
        super(MessagesAPIDeleteTest, self).setUp()
        self.messages_api = MessagesAPI(client=self.mock_client)

    def test_delete(self):
        response = self.messages_api.delete(3)

        self.mock_client.delete.assert_called_once_with("/messages/3")
        self.assertEquals(self.mock_delete_response, response)

    def test_delete_passing_id_as_a_dict(self):
        self.messages_api.delete({"id": 27})

        self.mock_client.delete.assert_called_once_with("/messages/27")

    def test_delete_passing_id_as_an_object(self):
        self.messages_api.delete(Mock(id=8))

        self.mock_client.delete.assert_called_once_with("/messages/8")


class MessagesAPILikeTest(TestCaseWithMockClient):
    def setUp(self):
        super(MessagesAPILikeTest, self).setUp()
        self.messages_api = MessagesAPI(client=self.mock_client)

    def test_like(self):
        response = self.messages_api.like(42)

        self.mock_client.post.assert_called_once_with(
            "/messages/liked_by/current",
            message_id=42,
        )
        self.assertEquals(self.mock_post_response, response)

    def test_like_passing_id_as_a_dict(self):
        self.messages_api.like({"id": 22})

        self.mock_client.post.assert_called_once_with(
            "/messages/liked_by/current",
            message_id=22,
        )

    def test_like_passing_id_as_an_object(self):
        self.messages_api.like(Mock(id=77))

        self.mock_client.post.assert_called_once_with(
            "/messages/liked_by/current",
            message_id=77,
        )

    def test_unlike(self):
        response = self.messages_api.unlike(42)

        self.mock_client.delete.assert_called_once_with(
            "/messages/liked_by/current",
            message_id=42,
        )
        self.assertEquals(self.mock_delete_response, response)

    def test_unlike_passing_id_as_a_dict(self):
        self.messages_api.unlike({"id": 22})

        self.mock_client.delete.assert_called_once_with(
            "/messages/liked_by/current",
            message_id=22,
        )

    def test_unlike_passing_id_as_an_object(self):
        self.messages_api.unlike(Mock(id=77))

        self.mock_client.delete.assert_called_once_with(
            "/messages/liked_by/current",
            message_id=77,
        )
