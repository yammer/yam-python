"""
Utilities used by the various APIs.
"""

class ArgumentDict(object):
    """
    A dictionary of arguments for an API call. As arguments are added they
    are converted to the type expected by the Yammer API.

    Booleans will be converted to strings:

        args["yes"] = True
        args["no"] = False

        args["yes"] is "true"
        args["no"] is "false"

    Lists and tuples will be split over multiple keys:

        args["topic"] == ("first", "second",)

        args["topic1"] is "first"
        args["topic2"] is "second"

    Dicts will be expanded:

        args["og"] = {"url": "http://example.com", "type": "example"}

        args["og_url"] is "http://example.com"
        args["og_type"] is "example"

    None will be discarded:

        args["null"] = None

        args["null"] # will raise a KeyError
    """

    def __init__(self, **kwargs):
        """
        Initializes a new argument dict. Keyword arguments will be added to
        the dict after being subjected to the usual conversions.
        """
        self._arguments = {}
        for key, value in kwargs.items():
            self[key] = value

    def keys(self):
        return self._arguments.keys()

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            self._add_dict(key, value)
        elif isinstance(value, (list, tuple)):
            self._add_list(key, value)
        else:
            self._add_value(key, value)

    def __getitem__(self, key):
        return self._arguments[key]

    def _add_value(self, key, value):
        if value is not None:
            self._arguments[key] = self._convert_value(value)

    def _add_list(self, key, values):
        for index, value in enumerate(values):
            item_key = "%s%d" % (key, index + 1)
            self._arguments[item_key] = self._convert_value(value)

    def _add_dict(self, prefix, values):
        for key, value in values.items():
            item_key = "%s_%s" % (prefix, key)
            self._arguments[item_key] = self._convert_value(value)

    def _convert_value(self, value):
        if value is True:
            return "true"
        elif value is False:
            return "false"
        else:
            return value
