"""
Shared support for live test cases.
"""

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
        def wrapper(self):
            if access_token:
                test_method(self, access_token)
            else:
                raise SkipTest("%s is not set" % variable)
        return wrapper
    return decorator
