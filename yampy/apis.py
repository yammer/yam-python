class MessagesAPI(object):
    """
    Provides an interface for accessing the message related endpoints of the
    Yammer API.
    """

    def __init__(self, client):
        """
        Initializes a new MessagesAPI that will use the given client object
        to make HTTP requests.
        """
        self._client = client

    def all(self, older_than=None, newer_than=None,
            limit=None, threaded=None):
        """
        Returns public messages from the current user's network.

        Customize the response using the keyword arguments:
        older_than -- Only fetch messages older than this message ID.
        newer_than -- Only fetch messages newer than this message ID.
        limit -- Only fetch this many messages.
        threaded -- Set to "true" to only receive the first message of each
            thread, or to "extended" to recieve the first and two newest
            messages from each thread.
        """
        return self._get(
            "/messages",
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        )

    def from_my_feed(self, older_than=None, newer_than=None,
                     limit=None, threaded=None):
        """
        Returns messages from the current user's feed. This will either
        correspond to from_top_conversations or from_followed_conversations
        depending on the user's settings.

        See the "all" method for a description of the keyword arguments.
        """
        return self._get(
            "/messages/my_feed",
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        )

    def from_top_conversations(self, older_than=None, newer_than=None,
                               limit=None, threaded=None):
        """
        Returns messages from the current user's top conversations.

        See the "all" method for a description of the keyword arguments.
        """
        return self._get(
            "/messages/algo",
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        )

    def from_followed_conversations(self, older_than=None, newer_than=None,
                                    limit=None, threaded=None):
        """
        Returns messages from users the current user follows, or groups
        the current user belongs to.

        See the "all" method for a description of the keyword arguments.
        """
        return self._get(
            "/messages/following",
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        )

    def sent(self, older_than=None, newer_than=None,
             limit=None, threaded=None):
        """
        Returns of the current user's sent messages.

        See the "all" method for a description of the keyword arguments.
        """
        return self._get(
            "/messages/sent",
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        )

    def private(self, older_than=None, newer_than=None,
                limit=None, threaded=None):
        """
        Returns of the private messages received by the current user.

        See the "all" method for a description of the keyword arguments.
        """
        return self._get(
            "/messages/private",
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        )

    def received(self, older_than=None, newer_than=None,
                 limit=None, threaded=None):
        """
        Returns messages received by the current user.

        See the "all" method for a description of the keyword arguments.
        """
        return self._get(
            "/messages/received",
            older_than=older_than,
            newer_than=newer_than,
            limit=limit,
            threaded=threaded,
        )

    def _get(self, path, **kwargs):
        filtered_kwargs = {k: v for (k, v) in kwargs.items() if v is not None}
        return self._client.get(path, **filtered_kwargs)
