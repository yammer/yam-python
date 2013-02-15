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
Shared support for live test cases.
"""

from functools import wraps
import os
from unittest.case import SkipTest

def skip_without_environment_variable(variable):
    """
    Decorator for a test methods, which makes execution conditional on an
    environment variable.

    When the environment variable is set, the test is run and the value of
    the variable is passed as an argument.

    When the environment variable is not set, the test is skipped.
    """
    def decorator(test_method):
        access_token = os.getenv(variable)
        @wraps(test_method)
        def wrapper(self):
            if access_token:
                test_method(self, access_token)
            else:
                raise SkipTest("%s is not set" % variable)
        return wrapper
    return decorator
