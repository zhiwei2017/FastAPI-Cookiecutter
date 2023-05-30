.. _usage-guide:

User Guide
==========

Tutorial
--------
Let's pretend you want to create a FastAPI project called "redditclone".
By using this template based on `cookiecutter`_,
you will be able to quickly setup a runnable FastAPI project.

First, get Cookiecutter. Trust me, it's awesome::

     $ pip install "cookiecutter>=1.7.0"

Now run it against this repo::

     $ cookiecutter https://github.com/zhiwei2017/FastAPI-Cookiecutter.git

You'll be prompted for some values. Provide them, then a FastAPI project will be created for you.

**Warning**: After this point, change 'My Awesome Project', 'John Doe', etc to your own information.

Answer the prompts with your own desired :ref:`Project Generation Options`. For example::

    Cloning into 'fastapi-cookiecutter'...
    remote: Enumerating objects: 219, done.
    remote: Counting objects: 100% (219/219), done.
    remote: Compressing objects: 100% (123/123), done.
    remote: Total 219 (delta 83), reused 181 (delta 69), pack-reused 0
    Receiving objects: 100% (219/219), 41.09 KiB | 1.71 MiB/s, done.
    Resolving deltas: 100% (83/83), done.
    project_name [My Awesome Project]: Reddit Clone
    project_slug [reddit_clone]: reddit_clone
    project_url [https://github.com/example_project]: https://github.com/redditclone
    author [John Doe]: John Doe
    email [john-doe@example.com]: john.doe@example.com
    short_description [Behold My Awesome Project!]: A reddit clone.
    version [0.0.1]: 0.1.0
    Select use_oauth:
    1 - No
    2 - Yes
    Choose from 1, 2 [1]: 1
    Select use_database:
    1 - Yes
    2 - No
    Choose from 1, 2 [1]: 1
    Select ci_tool:
    1. GitHub
    2. GitLab
    3. Bitbucket
    4. None
    Choose from 1, 2 [1]: 1
    Select python_version:
    1. 3.10
    2. 3.11
    3. 3.9
    4. 3.8
    5. 3.7
    Choose from 1, 2 [1]: 1

Enter the project and take a look around::

    $ cd reddit_clone/
    $ ls

Now take a look at your repo. Don't forget to carefully look at the generated **README**.

Literature
----------

+ `cookiecutter`_
+ `FastAPI <https://fastapi.tiangolo.com>`_
+ `Pydantic <https://pydantic-docs.helpmanual.io>`_
+ `SQLAlchemy <https://www.sqlalchemy.org>`_
+ `Alembic <https://alembic.sqlalchemy.org/en/latest/>`_
+ `PyJWT <https://github.com/jpadilla/pyjwt>`_
+ `python-jose <https://github.com/mpdavis/python-jose>`_


.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
