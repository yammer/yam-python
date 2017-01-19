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

"""
Utilities used by the various APIs.
"""

from functools import wraps
import re

from yampy.models import extract_id


def instance_replacer(*types):
    """
    Decorator for functions that passes all key/value pairs where the value
    has one of the given types to the decorated function. The decorated
    function should return a dict, which will be used as a replacement for
    the key/value pair that was pass to it.

    For example:
      @instance_replacer(bool)
      def boolean_inverter(key, value):
          return {"not_%s" % key: not value}

      boolean_inverter({"yes": True, "no": False, "other": 1})
      {"not_yes": False, "not_no": True, "other": 1}
    """
    def decorator(func):
        @wraps(func)
        def inner(arguments):
            result = {}
            for k, v in arguments.items():
                if isinstance(v, types):
                    result.update(func(k, v))
                else:
                    result[k] = v
            return result
        return inner
    return decorator


@instance_replacer(dict)
def flatten_dicts(prefix, collection):
    """
    Flattens nested dictionaries, joining the keys with an underscore.
    e.g. {"foo": {"bar": 1}}  becomes  {"foo_bar": 1}
    """
    result = {}
    for key, value in collection.items():
        item_key = "%s_%s" % (prefix, key)
        result[item_key] = value
    return result


@instance_replacer(list, tuple)
def flatten_lists(prefix, collection):
    """
    Expands all lists and tuples in a dictionary, so that each list item has
    its own key.
    e.g. {"foo": ("a", "b")}  becomes  {"foo1": "a", "foo2": "b"}
    """
    result = {}
    for index, value in enumerate(collection):
        item_key = "%s%d" % (prefix, index + 1)
        result[item_key] = value
    return result


@instance_replacer(bool)
def stringify_booleans(key, value):
    """
    Replaces all boolean values in a dictionary with lowercase strings.
    e.g. {"yes": True}  becomes  {"yes": "true"}
    """
    if value:
        return {key: "true"}
    else:
        return {key: "false"}


@instance_replacer(type(None))
def none_filter(key, value):
    """
    Removes None values from a dictionary.
    e.g. {"number": 1, "none": None}  becomes  {"number": 1}
    """
    return {}


class IDExtractor(object):
    """
    A callable object which, when called with a dict, will attempt to extract
    an ID from each value whose key matches the regular expression provided to
    the constructor.
    """

    def __init__(self, pattern=r'^.*_id$'):
        self._key_matcher = re.compile(pattern)

    def __call__(self, arguments):
        """
        Attempts to extract an ID from the value of any key that matches the
        pattern that was provided to the initialiser.
        e.g. With the default pattern of '^.*_id$'
             {"foo_id": {"id": 3}}  becomes  {"foo_id": 3}
        """
        result = arguments.copy()
        for key in arguments:
            if self._key_matcher.match(key):
                result[key] = extract_id(arguments[key])
        return result


class ArgumentConverter(object):
    """
    A callable object that takes a dict (in the form of keyword arguments),
    passes it through various converters and returns the result.
    """

    def __init__(self, *converters):
        """
        Initialize an ArgumentConverter that will call each of the given
        converters in turn. Converters should be callable, take a dict, and
        return a dict.
        """
        self._converters = converters

    def __call__(self, **kwargs):
        """
        Passes the dict of keyword arguments through each converter in turn,
        and returns the result.
        """
        converted_args = kwargs.copy()
        for converter in self._converters:
            converted_args = converter(converted_args)
        return converted_args
