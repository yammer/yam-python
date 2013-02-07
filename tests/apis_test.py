from mock import Mock
from unittest import TestCase

from yampy.apis import ArgumentDict, MessagesAPI
from yampy.errors import InvalidOpenGraphObjectError, TooManyTopicsError


class ArgumentDictTest(TestCase):
    def test_stores_values(self):
        args = ArgumentDict()
        args["foo"] = 123

        self.assertEquals(123, args["foo"])

    def test_ignores_none_values(self):
        args = ArgumentDict()
        args["foo"] = None

        with self.assertRaises(KeyError):
            args["foo"]

    def test_converts_booleans_to_strings(self):
        args = ArgumentDict()
        args["foo"] = True
        args["bar"] = False

        self.assertEquals("true", args["foo"])
        self.assertEquals("false", args["bar"])

    def test_stores_lists_as_multiple_keys(self):
        args = ArgumentDict()
        args["topic"] = ["testing", "python"]

        with self.assertRaises(KeyError):
            args["topic"]

        self.assertEquals("testing", args["topic1"])
        self.assertEquals("python", args["topic2"])

    def test_add_tuple(self):
        args = ArgumentDict()
        args["topic"] = ("first", "second", True, )

        with self.assertRaises(KeyError):
            args["topic"]

        self.assertEquals("first", args["topic1"])
        self.assertEquals("second", args["topic2"])
        self.assertEquals("true", args["topic3"])

    def test_add_empty_tuple(self):
        args = ArgumentDict()
        args["topic"] = ()

        with self.assertRaises(KeyError):
            args["topic"]

        with self.assertRaises(KeyError):
            args["topic1"]

    def test_add_dict(self):
        args = ArgumentDict()
        args["og"] = {"url": "http://www.google.com", "fetch": True}

        with self.assertRaises(KeyError):
            args["og"]

        self.assertEquals("http://www.google.com", args["og_url"])
        self.assertEquals("true", args["og_fetch"])

    def test_initializing_with_values(self):
        args = ArgumentDict(
            number=1,
            string="hello",
            topic=(True, False),
        )

        self.assertEquals(1, args["number"])
        self.assertEquals("hello", args["string"])
        self.assertEquals("true", args["topic1"])
        self.assertEquals("false", args["topic2"])

    def test_using_an_argument_dict_as_keyword_arguments(self):
        args = ArgumentDict()
        args["foo"] = 1
        args["bar"] = 2

        mock = Mock()
        mock(**args)

        mock.assert_called_once_with(foo=1, bar=2)


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
