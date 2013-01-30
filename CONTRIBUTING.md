# Contributing

## Quick Overview

We love pull requests. Here's a quick overview of the process (detail below):

1. Fork the repo.

2. Run the tests. We only take pull requests with passing tests, so start with a
clean slate.

3. Add a test for your new code. Only refactoring and documentation changes
require no new tests. If you are adding functionality or fixing a bug, we need a
test!

4. Make the test pass.

5. Push to your fork and submit a pull request.

At this point you're waiting on us. We may suggest some changes or improvements
or alternatives. Once we approve, we will merge your branch in.

Some things that will increase the chance that your pull request is accepted:

* Follow [PEP 8](http://www.python.org/dev/peps/pep-0008/).
* Use Pythonic idioms.
* Include tests which fail without your code and pass with it.
* Update the documentation, the surrounding code, examples elsewhere, guides,
  whatever is affected by your contribution.


## Requirements

Please remember this is open-source, so don't commit any passwords or API keys.
Those should go in environment variables.


## Development environment setup

Fork the repo and clone the app:

    git clone git@github.com:[GIT_USERNAME]/yam-python.git

Create a virtualenv:

    cd yam-python
    virtualenv ENV
    source ENV/bin/activate

When you're finished, deactivate the virtualenv:

    deactivate


## Running tests

Run the whole test suite with:

    python setup.py test

Run individual test modules like:

    python setup.py test -s tests.some_test_file


## Development process

For details and screenshots of the feature branch code review process, read
[this blog post](http://robots.thoughtbot.com/post/2831837714/feature-branch-code-reviews).
