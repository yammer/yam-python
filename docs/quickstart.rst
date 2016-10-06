.. _quickstart_guide:

Quickstart guide
================

Authentication
--------------

The Yammer API requires you to authenticate via OAuth 2, so you'll need a
``client_id`` and ``client_secret`` which you will be given when you register
your application with Yammer here: http://www.yammer.com/client_applications

To authenticate your application:

1. Build a :class:`yampy.Authenticator` using the ``client_id`` and
   ``client_secret`` you were given when you registered your application::

    import yampy

    authenticator = yampy.Authenticator(client_id=MY_CLIENT_ID,
                                        client_secret=MY_CLIENT_SECRET)

2. Send your user to the authorization URL where they can grant your application
   access to their Yammer account. You can construct the authorization URL using
   the ``Authenticator``, specifying the URL you want Yammer to return the user
   to when they are finished::

    redirect_uri = "http://example.com/auth/callback"
    auth_url = authenticator.authorization_url(redirect_uri=redirect_uri)

3. Once the user has authorized or denied your application, they will be sent to
   the ``redirect_url`` you specified. If the user has granted your application
   permission, a ``code`` parameter will be given in the query string. If
   something went wrong an ``error`` parameter will be passed instead. See the
   `authentication section of the Yammer API documentation
   <https://developer.yammer.com/authentication/>`_ for more information.

   Assuming everything went well, you can use the ``Authenticator`` to exchange
   your ``code`` for an access token::

    access_token = authenticator.fetch_access_token(code)

   If you require user and network information -- for example, if you want to
   store the Yammer user ID in your application's user model -- then you can use
   the ``fetch_access_data`` method instead::

    access_data = authenticator.fetch_access_data(code)

    access_token = access_data.access_token.token

    user_info = access_data.user
    network_info = access_data.network

Making requests
---------------

Once you have an access token you can create a :class:`yampy.Yammer` instance
and start making requests to the API::

    import yampy

    yammer = yampy.Yammer(access_token=access_token)

Messages
~~~~~~~~

You can make `message-related requests
<https://developer.yammer.com/restapi/#rest-messages>`_ using the ``messages``
property on your ``Yammer`` instance. These are just a few examples, see the
:class:`yampy.apis.MessagesAPI` class for details::

    import yampy

    yammer = yampy.Yammer(access_token=access_token)

    # Get a list of messages
    yammer.messages.all()
    yammer.messages.from_my_feed()
    yammer.messages.from_user(a_user)

    # Post a new messages
    yammer.messages.create("Hello developers", group_id=developers_group_id,
                           topics=["Python", "API", "Yammer"])

    # Delete a message
    yammer.messages.delete(a_message)

    # Like messages
    yammer.messages.like(a_message)
    yammer.messages.unlike(a_message)

Users
~~~~~

You can make `user-related requests
<https://developer.yammer.com/restapi/#rest-users>`_ using the ``users``
property on your ``Yammer`` instance. These are just a few examples, see the
:class:`yampy.apis.UsersAPI` class for details::

    import yampy

    yammer = yampy.Yammer(access_token=access_token)

    # Get a list of users
    yammer.users.all()
    yammer.users.in_group(a_group_id)

    # Find a specific user
    yammer.users.find(a_user_id)
    yammer.users.find_by_email("user@example.com")

    # Find the logged in user
    yammer.users.find_current()

    # Create a new user
    yammer.users.create("user@example.org", full_name="John Doe")

    # Update a user
    yammer.users.update(a_user, summary="An example user")

    # Suspend and delete users
    yammer.users.suspend(a_user)
    yammer.users.delete(a_user)

Groups
~~~~~

You can make `group-related requests using the ``groups``
property on your ``Yammer`` instance. These are just a few examples, see the
:class:`yampy.apis.GroupsAPI` class for details::

    import yampy

    yammer = yampy.Yammer(access_token=access_token)

    # Get a list of all groups in your network
    yammer.groups.all()
    # Get a list of all groups of current user
    yammer.groups.all(mine=True)

    # View a specific group
    yammer.groups.find(a_group_id)

    # Get members of specific group
    yammer.groups.members(a_group_id)

    # Join a specific group
    yammer.groups.join(a_group_id)

    # Leave a specific group
    yammer.groups.leave(a_group_id)

    # Create a new group
    yammer.groups.create("My new group", private=True)

    # delete a group
    yammer.groups.delete(a_group_id)

Other API endpoints
~~~~~~~~~~~~~~~~~~~

For other endpoints in the Yammer REST API, you will need to use Yampy's HTTP
API. Use the ``client`` property on your ``Yammer`` instance.

For example, to get a list of org chart relationships you would make this HTTP
request::

    GET https://www.yammer.com/api/v1/relationships.json?access_token=...

You can do this easily with the Yampy client::

    yammer = yampy.Yammer(access_token)
    yammer.client.get("/relationships")

See the `REST API documentation <https://developer.yammer.com/restapi/>`_ for a
full list of API endpoints, and the :class:`yampy.client.Client` class for details of
the Python interface.
