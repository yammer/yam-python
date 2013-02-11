from mock import Mock
from unittest import TestCase

from yampy.apis.utils import ArgumentDict


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
