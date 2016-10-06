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
        Initializes a new GroupsAPI that will use the given client object
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

    def members(self, group_id, page=None, reverse=None):
        """
        Returns the group identified by the given group_id.

        Customize the response using the keyword arguments:

        * page -- Enable pagination, and return the nth page of 50 users.
        """
        path = "/group_memberships"
        return self._client.get(path, **self._argument_converter(
            page=page,
            reverse=reverse,
        ))

    def join(self, group_id):
        """
        Join the group identified by the given group_id.

        Return True
        """
        path = "/group_memberships"
        group_id = extract_id(group_id)
        return self._client.post(path, **self._argument_converter(
            group_id=group_id,
        ))

    def leave(self, group_id):
        """
        Leave the group identified by the given group_id.

        Return True
        """
        path = "/group_memberships"
        group_id = extract_id(group_id)
        return self._client.delete(path, **self._argument_converter(
            group_id=group_id,
        ))

    def create(self, name, private=False):
        """
        Create a group.

        Return Group info
        """
        path = "/groups"
        return self._client.post(path, **self._argument_converter(
            name=name,
            private=private,
        ))

    def delete(self, group_id):
        """
        Delete a group.

        Return True if success
        """
        return self._client.delete(self._group_path(group_id), delete="true")

    def _group_path(self, group_id):
        return "/groups/%d" % extract_id(group_id)
