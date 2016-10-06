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

import json


class GenericModel(dict):
    """
    A dict subclass that provides access to its members as if they were
    attributes.

    Note that an attribute that has the same name as one of dict's existing
    method (``keys``, ``items``, etc.) will not be accessible as an attribute.
    """

    @classmethod
    def from_json(cls, json_string):
        """
        Parses the given json_string, returning GenericModel instances instead
        of dicts.
        """
        return json.loads(json_string, object_hook=cls)

    def __getattr__(self, prop):
        """
        Provides access to the members of the dict as attributes.
        """
        if prop in self:
            return self[prop]
        else:
            raise AttributeError


def extract_id(source):
    """
    Attempts to extract an ID from the argument, first by looking for an
    attribute and then by using dictionary access. If both fail, the argument
    is returned.
    """
    try:
        return source.id
    except AttributeError:
        pass

    try:
        return source["id"]
    except (TypeError, KeyError) as err:
        pass

    return source
