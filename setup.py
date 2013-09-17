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

import os

from setuptools import setup

VERSION = "1.0"

def readme():
    """ Load the contents of the README file """
    readme_path = os.path.join(os.path.dirname(__file__), "README.txt")
    with open(readme_path, "r") as f:
        return f.read()

setup(
    name="yampy",
    version=VERSION,
    description="The official Python client for Yammer's API",
    author="Yammer",
    author_email="blyttle@yammer-inc.com",
    long_description=readme(),
    packages=["yampy", "yampy.apis"],
    install_requires=["requests"],
    license="Apache",
    url="http://github.com/yammer/yam-python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
    ],

    tests_require=["nose", "mock", "flask"],
    test_suite="nose.collector",
)
