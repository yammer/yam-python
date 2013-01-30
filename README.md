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

        import yampy.Authenticator

        authenticator = yampy.Authenticator(client_id=MY_CLIENT_ID,
                                            client_secret=MY_CLIENT_SECRET)

2.  Send your user to the authorization URL where they can grant your
    application access to their Yammer account. You can construct the
    authorization URL using the `yampy.Authenticator`, specifying the URL you
    want Yammer to return the user to when they are finished:

        return_uri = "http://example.com/auth/callback"
        auth_url = authenticator.authorization_url(return_uri=return_uri)

3.  Once the user has authorized or denied your application, they will be sent
    to the `return_uri` you specified. If the user has granted your application
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

Once you have an access token you can create a `yampy.Client` and start making
requests to the API:

```python
import yampy.Client

yammer = yampy.Client(access_token=access_token)
```

You can also pass the `base_url` keyword argument to change the base URL
requests are sent to. By default this is `"https://www.yammer.com/api/v1"`. For
example, in your test suite you might want to run a fake Yammer API server
locally to speed up your tests:

```python
yammer = yampy.Client(access_token=access_token,
                      base_url="http://localhost:5001")
```

Use the `yampy.Client` instance to make requests to any of the API endpoints.
For a complete list of Yammer API endpoints, see the [REST API
documentation](http://developer.yammer.com/restapi/). Here are a few examples:

```python
# Find a user by ID
yammer.get("/users/123456")

# Find a user by email
yammer.get("/users/by_email", email="user@example.com")

# Post a status message
yammer.post("/messages", body="Trying out yampy")

# Send a private message to a user
yammer.post("/messages", body="Just for you", direct_to_id=123456)

# Send a private message to a group
yammer.post("/messages", body="Hey developers!", group_id=98765)

# Send a message with an attached Open Graph Object
yammer.post("/messages", body="Check this out",
            og_url="http://example.com/graph/12345")
```

## Contributing

To contribute to this project, see the
[CONTRIBUTING.md](https://github.com/yammer/yam-python/blob/master/CONTRIBUTING.md)
file.

[API-auth]: https://developer.yammer.com/authentication/
