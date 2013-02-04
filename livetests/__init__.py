"""
Tests that run against the live Yammer API. These aren't intended to be run
frequently during development, they exist to automate the process of checking
that the assumptions made by the library still accurately reflect the live
implementation.

A YAMMER_ACCESS_TOKEN environment variable is required to run these tests. They
run against the live API and post real messages, so don't use an account that
you really care about.
"""
