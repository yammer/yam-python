.. _contributing_guide:

Contributing guide
==================

Quick overview
--------------

We love pull requests. Here's a quick overview of the process (detail below):

1. Fork the `GitHub repository <https://www.github.com/yammer/yam-python>`_.
2. Run the tests. We only take pull requests with passing tests, so start with a
   clean slate.
3. Add a test for your new code. Only refactoring and documentation changes
   require no new tests. If you are adding functionality of fixing a bug, we
   need a test!
4. Make the test pass.
5. Push to your fork and submit a pull request.

At this point you're waiting on us. We may suggest some changes or improvements
or alternatives. Once we approve, we will merge your branch in.

Some things that will increase the chance that your pull request is accepted:

* Follow `PEP 8 <http://www.python.org/dev/peps/pep-00008/>`_.
* Use Pythonic idioms.
* Include tests which fail without your code and pass with it.
* Update the documentation, the surrounding code, examples elsewhere, guides,
  whatever is affected by your contribution.


Requirements
------------

Please remember this is open-source, so don't commit any passwords or API keys.
Those should go in environment variables.


Development environment setup
-----------------------------

Fork the repo and clone the app::

    git clone git@github.com:[GIT_USERNAME]/yam-python.git

Create a virtualenv::

    cd yam-python
    virtualenv ENV
    source ENV/bin/activate

Install the development dependencies in your virtualenv::

    pip install -r requirements_dev.txt

When you've finished working on Yampy, deactivate the virtualenv::

    deactivate


Running tests
-------------

Run the whole test suite with::

    nosetests

You can also pass the name of a module, class, or a path to a directory or
file::

    nosetests tests.apis.messages_test.MessagesAPICreateTest
    nosetests tests/apis
    nosetests tests/apis/messages_test.py

There is also a live integration test suite. This shouldn't be run frequently
during development, but is useful for checking that the assumptions made in the
client still match the live API. Since it is run against the live API and posts
real messages, it requires an access token and shouldn't be run against an
account that you are actively using. Run the live integration tests with::

    YAMMER_ACCESS_TOKEN=abc123xyz nosetests livetests


Development process
-------------------

For details and screenshots of the feature branch code review process, read
`this blog post
<http://robots.thoughtbot.com/post/2831837714/feature-branch-code-reviews>`_.
