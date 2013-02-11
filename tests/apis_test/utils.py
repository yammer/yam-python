from mock import Mock
from unittest import TestCase

from yampy.apis.utils import ArgumentConverter, flatten_lists, flatten_dicts, \
                             stringify_booleans, none_filter


class ArgumentConverterNoConvertersTest(TestCase):
    """
    Tests the ArgumentConverter with no converters.
    """

    def setUp(self):
        self.converter = ArgumentConverter()

    def test_does_not_change_any_values(self):
        result = self.converter(
            boolean=True,
            number=1,
            string="hello",
            list=[1, 2, 3],
            tuple=(True, False),
            empty_tuple=(),
            none=None,
        )

        self.assertEquals(True, result["boolean"])
        self.assertEquals(1, result["number"])
        self.assertEquals("hello", result["string"])
        self.assertEquals([1, 2, 3], result["list"])
        self.assertEquals((True, False), result["tuple"])
        self.assertEquals((), result["empty_tuple"])
        self.assertEquals(None, result["none"])


class ArgumentConverterFlattenDictsTest(TestCase):
    """
    Tests the ArgumentConverter using the flatten_dicts converter.
    """

    def setUp(self):
        self.converter = ArgumentConverter(flatten_dicts)

    def test_converts_dict_to_multiple_keys(self):
        result = self.converter(og={"url": "http://www.google.com", "fetch": True})

        with self.assertRaises(KeyError):
            result["og"]

        self.assertEquals("http://www.google.com", result["og_url"])
        self.assertEquals(True, result["og_fetch"])


class ArgumentConverterFlattenListsTest(TestCase):
    """
    Tests the ArgumentConverter using the flatten_lists converter.
    """

    def setUp(self):
        self.converter = ArgumentConverter(flatten_lists)

    def test_converts_list_to_multiple_keys(self):
        result = self.converter(
            topic=["testing", "python"],
        )

        with self.assertRaises(KeyError):
            result["topic"]

        self.assertEquals("testing", result["topic1"])
        self.assertEquals("python", result["topic2"])

    def test_converts_tuple_to_multiple_keys(self):
        result = self.converter(topic=("first", "second", ))

        with self.assertRaises(KeyError):
            result["topic"]

        self.assertEquals("first", result["topic1"])
        self.assertEquals("second", result["topic2"])

    def test_ignores_empty_tuples(self):
        result = self.converter(topic=())

        with self.assertRaises(KeyError):
            result["topic"]

        with self.assertRaises(KeyError):
            result["topic1"]


class ArgumentConverterStringifyBooleansTest(TestCase):
    """
    Tests the ArgumentConverter using the stringify_booleans converter.
    """

    def setUp(self):
        self.converter = ArgumentConverter(stringify_booleans)

    def test_converts_booleans_to_strings(self):
        result = self.converter(
            yes=True,
            no=False,
        )

        self.assertEquals("true", result["yes"])
        self.assertEquals("false", result["no"])


class ArgumentConverterNoneFilterTest(TestCase):
    """
    Tests the ArgumentConverter using the none_filter converter.
    """

    def setUp(self):
        self.converter = ArgumentConverter(none_filter)

    def test_ignores_none_values(self):
        result = self.converter(foo=None)

        with self.assertRaises(KeyError):
            result["foo"]


class ArgumentConverterCompositionTest(TestCase):
    """
    Tests the ArgumentConverter using multiple converters.
    """

    def setUp(self):
        self.converter = ArgumentConverter(
            flatten_dicts,
            flatten_lists,
            none_filter,
        )

    def test_applies_each_converter_in_turn(self):
        result = self.converter(
            a_dict={
                "a_list": [1, 2, None],
            },
        )

        self.assertEquals(
            {
                "a_dict_a_list1": 1,
                "a_dict_a_list2": 2,
            },
            result
        )
