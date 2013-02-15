import json


class GenericModel(dict):
    """
    A dict subclass that provides access to its members as if they were
    attributes.

    Note that an attribute that has the same name as one of dict's existing
    method (``keys``, ``items``, etc.) will not be accessible as an attribute.
    """

    @classmethod
    def from_json(cls, json_string):
        """
        Parses the given json_string, returning GenericModel instances instead
        of dicts.
        """
        return json.loads(json_string, object_hook=cls)

    def __getattr__(self, prop):
        """
        Provides access to the members of the dict as attributes.
        """
        if prop in self:
            return self[prop]
        else:
            raise AttributeError
