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

1. Construct the following URL using the `client_id` you received after
registering your app with Yammer, and a URI you want Yammer to redirect the user
to after they've authorized your application:
`https://www.yammer.com/dialog/oauth?client_id=[:client_id]&redirect_uri=[:redirect_uri]`

2. Send the user to the URI you constructed above. When they click the "Allow"
button they will be redirected to the `redirect_uri` you provided, with a `code`
query string parameter. If they deny your app access, or something else goes
wrong, there will be an `error` parameter instead, which you should handle.

3. Use the `code` along with your `client_id` and `client_secret` to construct
the following URL:
`https://www.yammer.com/oauth2/access_token.json?client_id=[:client_id]&client_secret=[:client_secret]&code=[:code]`

4. Fetch the access token using the URL constructed above. The response will be
a JSON blob containing user and network information, and an access token
(`"abcdefghijklmn"` in this example):

        {
            "user": {
                ...
            },
            "network": {
                ...
            },
            "access_token": {
                "access_token": "abcdefghijklmn",
                ...
            }
        }

### Making requests

Once you have an access token you can create a `yampy.Client` and start making
requests to the API:

```python
import yampy.Client

yammer = yampy.Client(access_token="abcdefghijklmn")
```

You can also pass the `base_url` keyword argument to change the base URL
requests are sent to. By default this is `"https://www.yammer.com/api/v1"`. For
example, in your test suite you might want to run a fake Yammer API server
locally to speed up your tests:

```python
yammer = yampy.Client(access_token="abcdefghijklmn",
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
