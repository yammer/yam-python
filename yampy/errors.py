# Copyright (c) Microsoft Corporation
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY
# IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR
# PURPOSE, MERCHANTABLITY OR NON-INFRINGEMENT.
#
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.

"""
Exception classes representing error responses from the Yammer API.
"""

class ResponseError(Exception):
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
    Raised when a request is made with an access token that has expired or has
    been revoked by the user.
    """
    pass


class RateLimitExceededError(ResponseError):
    """
    Raised when a request is rejected because the rate limit has been
    exceeded.
    """
    pass


class InvalidMessageError(Exception):
    """
    Super class for the various kinds of errors that can occur when creating
    a message.
    """
    pass


class TooManyTopicsError(InvalidMessageError):
    """
    Raised when a message cannot be created because too many topics have been
    specified.
    """
    pass


class InvalidOpenGraphObjectError(InvalidMessageError):
    """
    Raised when an invalid Open Graph object is attached to a new message.
    """
    pass

class InvalidUserError(Exception):
    """
    Super class for the various kinds of errors that can occur when creating
    a user.
    """
    pass

class InvalidEducationRecordError(InvalidUserError):
    """
    Raised when creating a user with an education record that doesn't include
    all of the requried information.
    """
    pass

class InvalidPreviousCompanyRecord(InvalidUserError):
    """
    Raised when creating a user with a previous_companies record that doesn't
    include all of the required fields.
    """
    pass
