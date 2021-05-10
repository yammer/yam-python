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


class RelationshipsAPI(object):
    """
    Provides an interface for accessing the relations related endpoints of the
    Yammer API. You should not instantiate this class directly; use the
    :meth:`yampy.Yammer.relationships` method instead.
    """

    def __init__(self, client):
        """
        Initializes a new RelationshipsAPI that will use the given ``client`` object
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

    def all(self, user_id=None):
        """
        Returns the relationships for the current user or the user specified
        """
        return self._client.get("/relationships", **self._argument_converter(
            user_id=user_id,
        ))
