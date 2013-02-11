from yampy.apis.utils import ArgumentConverter, flatten_dicts, \
                             stringify_booleans, none_filter


class UsersAPI(object):
    def __init__(self, client):
        """
        Initializes a new UsersAPI that will use the given client object
        to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter(
            flatten_dicts,
            stringify_booleans,
            none_filter,
        )

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
        return self._client.get("/users", **self._argument_converter(
            page=page,
            letter=letter,
            sort_by=sort_by,
            reverse=reverse,
        ))

    def in_group(self, group_id, page=None):
        """
        Returns all the users belonging to the group identified by the given
        group_id.

        Use the page parameter to enable pagination and retrieve a specific
        page of users.
        """
        path = "/users/in_group/%d" % group_id
        return self._client.get(path, **self._argument_converter(
            page=page,
        ))

    def find_current(self):
        """
        Returns the current user.
        """
        return self._client.get("/users/current")

    def find(self, user_id):
        """
        Returns the user identified by the given user_id.
        """
        return self._client.get("/users/%d" % user_id)

    def find_by_email(self, email_address):
        """
        Returns the user identified by the given email_address.
        """
        return self._client.get("/users/by_email", **self._argument_converter(
            email=email_address,
        ))

    def create(self, email_address, full_name=None, job_title=None,
               location=None, im=None, work_telephone=None, work_extension=None,
               mobile_telephone=None, significant_other=None, kids_names=None,
               interests=None, summary=None, expertise=None, education=None):
        """
        Creates a new user.

        Most of the parameter names are self explanatory, and accept strings. A
        few expect specific formats:
        im -- Provide instant messages details as a dict with "provider" and
            "username" keys, e.g.
            {"provider": "gtalk", "username": "me@gmail.com"}
        """
        return self._client.post("/users", **self._argument_converter(
            email=email_address,
            full_name=full_name,
            job_title=job_title,
            location=location,
            im=im,
            work_telephone=work_telephone,
            work_extension=work_extension,
            mobile_telephone=mobile_telephone,
            significant_other=significant_other,
            kids_names=kids_names,
            interests=interests,
            summary=summary,
            expertise=expertise,
        ))
