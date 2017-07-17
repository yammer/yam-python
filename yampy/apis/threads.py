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

from yampy.apis.utils import ArgumentConverter, IDExtractor, flatten_lists, \
                             flatten_dicts, stringify_booleans, none_filter


class ThreadsAPI(object):
    """
    Provides an interface for accessing the threads related endpoints of the
    Yammer API. You should not instantiate this class directly; use the
    :meth:`yampy.Yammer.threads` method instead.
    """

    def __init__(self, client):
        """
        Initializes a new threadsAPI that will use the given ``client`` object
        to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter(
            IDExtractor(r"^(older|newer)_than|.*_id$"),
            flatten_lists,
            flatten_dicts,
            stringify_booleans,
            none_filter,
        )

    def find(self, thread_id):
        """
        Returns the thread identified by the given thread_id.
        """
        path = "/threads/%d" % thread_id
        return self._client.get(path, **self._argument_converter(
        ))