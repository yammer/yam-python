import os

from setuptools import setup

VERSION = "0.1"

def readme():
    """ Load the contents of the README file """
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "r") as f:
        return f.read()

setup(
    name="yampy",
    version=VERSION,
    description="The official Python client for Yammer's API",
    long_description=readme(),
    packages=["yampy"],
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
