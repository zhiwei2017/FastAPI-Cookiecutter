Contributing
============

Contributions are welcome, and they are greatly appreciated!

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/zhiwei2017/fastapi-cookiecutter

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the `GitHub <fastapi-cookiecutter>`_ issues for bugs. Anything tagged with **bug**
and **help wanted** is open to whoever wants to implement a fix for it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the `GitHub <fastapi-cookiecutter>`_ issues for features. Anything tagged with **enhancement**
and **help wanted** is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Pyckage Cookiecutter could always use more documentation, whether as part of
the official docs, in docstrings, or even on the web in blog posts, articles,
and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/zhiwei2017/fastapi-cookiecutter/issues.

If you are proposing a new feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

Get Started!
------------

Ready to contribute? Here's how to set up `fastapi-cookiecutter`_ for local
development. Please note this documentation assumes you already have git_ installed and ready to go.

1. Fork the `fastapi-cookiecutter`_ repo on `GitHub <fastapi-cookiecutter>`_.

2. Clone your fork locally:

   .. code-block:: bash

    $ cd path_for_the_repo
    $ git clone git@github.com:YOUR_NAME/fastapi-cookiecutter.git

3. You can create a new environment for your local
   development by typing:

   .. code-block:: bash

        $ venv fastapi-cookiecutter-venv
        $ source fastapi-cookiecutter-venv/bin/activate

   This should change the shell to look something like:

   .. code-block:: bash

        (fastapi-cookiecutter-env) $

4. Create a branch for local development:

   .. code-block:: bash

        $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass all linting checks:

   .. code-block:: bash

        $ make flake8
        $ make mypy
        $ make bandit

6. The next step would be to run the test cases:

   .. code-block:: bash

        $ make test

7. Before raising a pull request you should also run **docker-compose**. This will run the
   tests across different versions of Python:

   .. code-block:: bash

        $ docker compose up
        $ docker compose down

   If you are missing flake8, bandit, mypy, pytest, just `pip install` them into
   your virtual environment.

8. If your contribution is a bug fix or new feature, you may want to add a test
   to the existing test suite. See section Add a New Test below for details.

9. Commit your changes and push your branch to `GitHub <fastapi-cookiecutter>`_:

   .. code-block:: bash

        $ git add .
        $ git commit -m "Your detailed description of your changes."
        $ git push origin name-of-your-bugfix-or-feature

10. Submit a pull request through the `GitHub <fastapi-cookiecutter>`_ website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated. Put your
   new functionality into a function with a docstring.

3. The pull request should work for Python 3.7, 3.8, 3.9, 3.10 and 3.11.

Add a New Test
--------------

When fixing a bug or adding features, it's good practice to add a test to
demonstrate your fix or new feature behaves as expected. These tests should
focus on one tiny bit of functionality and prove changes are correct.

To write and run your new test, follow these steps:

1. Add the new test to `tests`. Focus your test on the
   specific bug or a small part of the new feature.

2. Run your test and confirm that your test does not fail:

   .. code-block:: bash

        $ make test

3. Run the tests with **docker-compose** to ensure that the code changes work with
   different Python versions:

   .. code-block:: bash

        $ docker compose up
        $ docker compose down

Deploying
---------

Assume that bump2version_ is installed. To deploy the package, just run::

    $ bump2version patch  # possible: major / minor / patch
    $ git push
    $ git push --tags

Github Actions will do the rest.

.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _fastapi-cookiecutter: https://github.com/zhiwei2017/fastapi-cookiecutter
.. _bump2version: https://github.com/c4urself/bump2version
