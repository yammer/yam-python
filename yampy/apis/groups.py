from yampy.apis.utils import ArgumentConverter, none_filter, stringify_booleans
from yampy.models import extract_id


class GroupsAPI(object):

    """
    Provides an interface for accessing the groups related endpoints of the
    Yammer API. You should not instantiate this class directly; use the
    :meth:`yampy.Yammer.groups` method instead.
    """

    def __init__(self, client):
        """
        Initializes a new UsersAPI that will use the given client object
        to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter(
            none_filter, stringify_booleans,
        )

    def all(self, mine=None, reverse=None):
        """
        Returns all the groups in the current user's network.

        Customize the response using the keyword arguments:

        * mine -- Only return group of current user.
        * reverse -- return group in descending order by name.
        """
        return self._client.get("/groups", **self._argument_converter(
            mine=mine,
            reverse=reverse,
        ))

    def find(self, group_id):
        """
        Returns the group identified by the given group_id.
        """
        return self._client.get(self._group_path(group_id))

    def members(self, group_id, page=None):
        """
        Returns the group identified by the given group_id.

        Customize the response using the keyword arguments:

        * page -- Enable pagination, and return the nth page of 50 users.
        """
        path = "/groups/%d/members" % extract_id(group_id)
        return self._client.get(path, **self._argument_converter(
            page=page,
        ))

    def _group_path(self, group_id):
        return "/groups/%d" % extract_id(group_id)
