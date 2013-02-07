from yampy.apis.utils import ArgumentDict


class UsersAPI(object):
    def __init__(self, client):
        """
        Initializes a new UsersAPI that will use the given client object
        to make HTTP requests.
        """
        self._client = client

    def all(self, page=None, letter=None, sort_by=None, reverse=None):
        """
        Returns all the users in the current user's network.

        Customize the response using the keyword arguments:
        page -- Enable pagination, and return the nth page of 50 users.
        letter -- Only return users whose username begins with this letter.
        sort_by -- Sort users by "messages" or "followers" (default order is
            alphabetical by username).
        reverse -- Reverse sort order.
        """
        return self._client.get("/users", **ArgumentDict(
            page=page,
            letter=letter,
            sort_by=sort_by,
            reverse=reverse,
        ))
