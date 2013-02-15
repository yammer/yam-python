# Yampy

Yampy (“Yam Pie”) is the official Python library for interacting with
Yammer's API.

## Installation

Install with pip:

```sh
pip install yampy
```

Or with easy_install:

```sh
easy_install yampy
```

Or manually:

```sh
git clone git://github.com/yammer/yam-python.git
cd yam-python
python setup.py install
```

## Usage

### OAuth 2 authentication

The Yammer API requires you to authenticate via OAuth 2, so you'll need a
`client_id` and `client_secret` which you will be given when you register your
application with Yammer here: <https://www.yammer.com/client_applications>

To authenticate a user of your application:

1.  Build a `yampy.Authenticator` using the `client_id` and `client_secret` you
    were given when you registered your application:

        import yampy

        authenticator = yampy.Authenticator(client_id=MY_CLIENT_ID,
                                            client_secret=MY_CLIENT_SECRET)

2.  Send your user to the authorization URL where they can grant your
    application access to their Yammer account. You can construct the
    authorization URL using the `yampy.Authenticator`, specifying the URL you
    want Yammer to return the user to when they are finished:

        redirect_uri = "http://example.com/auth/callback"
        auth_url = authenticator.authorization_url(redirect_uri=redirect_uri)

3.  Once the user has authorized or denied your application, they will be sent
    to the `redirect_uri` you specified. If the user has granted your application
    permission, a `code` parameter will be given in the query string. If
    something went wrong an `error` parameter will be passed instead,
    which you should handle. See the [authentication section of the Yammer API
    documentation][API-auth] for more information.

    Assuming everything went well, you can use the `yampy.Authenticator` to
    exchange your `code` for an access token:

        access_token = authenticator.fetch_access_token(code)

    If you require user and network information -- for example, if you want to
    store the Yammer user ID in your application's user model -- then you can
    use the `fetch_access_data` method instead:

        access_data = authenticator.fetch_access_data(code)

        access_token = access_data["access_token"]["token"]

        user_info = access_data["user"]
        network_info = access_data["network"]

### Making requests

Once you have an access token you can create a `yampy.Yammer` instance and start
making requests to the API:

```python
import yampy

yammer = yampy.Yammer(access_token=access_token)
```

You can also pass the `base_url` keyword argument to change the base URL
requests are sent to. By default this is `"https://www.yammer.com/api/v1"`. For
example, in your test suite you might want to run a fake Yammer API server
locally to speed up your tests:

```python
yammer = yampy.Yammer(access_token=access_token,
                      base_url="http://localhost:5001")
```

#### Messages

You can make [message-related requests][API-messages] use this domain specific
API. Many of these methods take keyword arguments to customised the results,
see the built in documentation (`help(yammer.messages)`) for details.

```python
# Get a list of messages
yammer.messages.all()
yammer.messages.from_my_feed()
yammer.messages.from_top_conversations()
yammer.messages.from_followed_conversations()
yammer.messages.sent()
yammer.messages.private()
yammer.messages.received()
yammer.messages.in_thread(a_thread_id)
yammer.messages.from_user(a_user_id)

# Get a specific message
yammer.messages.find(a_message_id)

# Post a new message
yammer.messages.create("Hello world!")
yammer.messages.create("Hello developers", group_id=developers_group_id,
                       topics=["Python", "API", "Yammer"])

# Delete a message
yammer.messages.delete(a_message_id)

# Like messages
yammer.messages.like(a_message_id)
yammer.messages.unlike(a_message_id)
```

#### Users

[User related requests][API-users] also have a specific API. As with messages,
these methods accept many keyword arguments. See the build in documentation for
details.

```python
# Get a list of users
yammer.users.all()
yammer.users.in_group(a_group_id)

# Get the logged in user
yammer.users.find_current()

# Get a specific individual user
yammer.users.find(a_user_id)
yammer.users.find_by_email("user@example.com")

# Create a new user
yammer.users.create("user@example.org", full_name="John Doe")

# Update a user
yammer.users.update(a_user_id, summary="An example user")

# Suspend and delete users
yammer.users.suspend(a_user_id)
yammer.users.delete(a_user_id)
```

#### Making other requests

For other endpoints in the Yammer REST API, you will need to use the HTTP API.
The `yampy.Client` class will help you do this.

For example, to get a list of org chart relationships you would make this HTTP
request:

    GET https://www.yammer.com/api/v1/relationships.json?access_token=...

You can do this easily with the yampy client:

    yammer.client.get("/relationships")

If you need to add parameters to the request, you can pass them as keyword
arguments. For example:

    yammer.client.get("/suggestions", limit=20)

See the [REST API documentation][API-REST] for a full list of API endpoints.

## Contributing

To contribute to this project, see the
[CONTRIBUTING.md](https://github.com/yammer/yam-python/blob/master/CONTRIBUTING.md)
file.

[API-auth]: https://developer.yammer.com/authentication/
[API-messages]: https://developer.yammer.com/restapi/#rest-messages
[API-users]: https://developer.yammer.com/restapi/#rest-users
[API-REST]: https://developer.yammer.com/restapi/
