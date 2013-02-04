"""
Exception classes representing error responses from the Yammer API.
"""

class ResponseError(StandardError):
    """
    Raised when the Yammer API responds with an HTTP error, and there
    isn't a more specific subclass that represents the situation.
    """
    pass

class NotFoundError(ResponseError):
    """
    Raised when the Yammer API responds with an HTTP 404 Not Found error.
    """
    pass

class UnauthorizedError(ResponseError):
    """
    Raised when the Yammer API responds with an HTTP 401 Unauthorized error.
    This may mean that the access token you are using is invalid.
    """
    pass

class InvalidAccessTokenError(ResponseError):
    """
    Raised when a request is made with an expired or otherwise invalid
    OAuth access token.
    """
    pass

class RateLimitExceededError(ResponseError):
    """
    Raised when a request is rejected because the rate limit has been
    exceeded.
    """
    pass
