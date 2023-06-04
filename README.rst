FastAPI Cookiecutter Template
=============================

Introduction
------------
This projects consist of a `cookiecutter`_ template that generates a full structure
for creating a RESTful API service project based on FastAPI following the MVC
(Model-View-Controller) structure in the same way Django projects does.

While using this project, you will be asked to provide some inputs such the authors, the name of the project, etc. As result you will obtain the
complete file and folder structure to quickly start to code your project.

Prerequisites
-------------
It uses ``Python`` (>=3.7) behind the scenes. Please install the Python package `cookiecutter`_ before using it.



Project Generation Options
--------------------------

project_name:
  Your project's human-readable name, capitals and spaces allowed.

project_slug:
    Your project's slug without dashes or spaces. Used to name your repo
    and in other places where a Python-importable version of your project name
    is needed.

project_url:
    The url of your project hosted in gitlab or github.

author:
    This is you! The value goes into places like ``README.md`` and such.

email:
    The email address you want to identify yourself in the project.

short_description:
    Describes your project briefly and gets used in places like ``README.md`` and ``setup.py``.

version:
    The version of the project at its inception.

use_oauth:
    Indicates whether the project should be configured for using OAuth2 authentication. The choices are:

    1. No
    2. Yes

use_database:
    Indicates whether the project should be configured for using database. The choices are:

    1. No
    2. Yes

ci_tool:
    Select a CI tool. The choices are:

    1. GitHub
    2. GitLab
    3. Bitbucket
    4. None

ci_tool:
    Select the python version for configuring the created project's CI/CD pipeline. The choices are:

    1. 3.10
    2. 3.11
    3. 3.9
    4. 3.8
    5. 3.7

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

Answer the prompts with your own desired `Project Generation Options <./docs/source/02_prompts.rst>`_. For example::

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

Project Structure
-----------------

Files related to application are in the ``src`` or ``tests`` directories.
Application components are::

    {{cookiecutter.project_slug}}
    ├── docs                            - sphinx documentastion
    ├── scripts                         - scripts
    │   └── prestart.sh
    ├── {{cookiecutter.project_slug}}
    │   ├── app
    │   │   ├── api                     - api endpoints
    │   │   │   └── base.py             - basic endpoints
    │   │   ├── application.py          - function for FastAPI application creation and configuration
    │   │   ├── configs                 - application configuration
    │   │   │   └── base.py             - basic configuration class
    │   │   ├── constants.py            - constants used inside the application
    │   │   ├── db                      - database related stuff
    │   │   │   ├── base.py             - base sqlalchemy DB model class
    │   │   │   ├── models              - folder for defining sqlalchemy DB model classes
    │   │   │   ├── queries             - folder for predefined sqlalchemy queries
    │   │   │   └── session.py          - a local session instance used inside application
    │   │   ├── events                  - events for startup, shutdown
    │   │   │   └── base.py             - dummy startup event and shudown event
    │   │   ├── globals.py              - global variables
    │   │   ├── middlewares             - middleware stuff
    │   │   │   └── logging.py          - middleware function related to logging
    │   │   ├── schemas                 - pydantic models for this application
    │   │   │   └── base.py             - pydantic models for the basic endpoints
    │   │   ├── services                - logic that is not included in the other folders
    │   │   ├── utils                   - utility stuff
    │   │   │   ├── errors.py           - customized exception classes
    │   │   │   ├── logging.py          - logging related utility functions, classes
    │   │   │   └── security.py         - security related functions, classes
    │   │   └── version.py              - version information
    │   ├── data                        - data used for this application
    │   └── main.py                     - main function to run the application
    ├── tests                           - unit tests
    │   ├── conftest.py                 - fixtures in tests
    │   ├── resources                   - resources used in tests
    │   └── ...
    ├── Dockerfile                      - docker file for building docker image
    ├── Makefile                        - predefined commands
    ├── README.md                       - package information
    ├── requirements                - package dependencies
    │   ├── base.txt                - documentation dependecies
    │   ├── doc.txt                 - documentation dependecies
    │   ├── dev.txt                 - tests dependencies
    ├── setup.cfg                       - configurations for mypy, bandit, pytest etc. Centralizing all the configurations to one place.
    └── setup.py                        - package installation configuration

Advanced Usage
--------------
``Gunicorn`` Configuration
**************************
A default ``gunicorn-conf.py`` file is included in the docker image and will be
executed before your service is up. It supports configuration through environment
variables. Please check the section `Environment variables <https://github.com/tiangolo/uvicorn-gunicorn-docker#environment-variables>`_
from `uvicorn-gunicorn-docker`_ project
for more detailed information. The suggested approach for defining environment variables
is to use the ``scrtips/prestart.sh`` file.

In case you need to customize the ``Gunicorn`` configuration file, please check the
default `gunicorn-conf.py <https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/gunicorn_conf.py>`_ file
and read the section `Custom Gunicorn configuration file <https://github.com/tiangolo/uvicorn-gunicorn-docker#custom-gunicorn-configuration-file>`_
from `uvicorn-gunicorn-docker`_ project firstly.

Customize ``prestart`` Hook
***************************
If you need to run anything before starting the app, you can add a file ``prestart.sh`` to the directory ``scripts``.
Please check the section `Custom /app/prestart.sh <https://github.com/tiangolo/uvicorn-gunicorn-docker#custom-appprestartsh>`_
from `uvicorn-gunicorn-docker`_ project for more details.

Access Token
************
An access token creation function is provided. However, it's not used by fault.
To use it, please check the `example <the https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/api/api_v1/endpoints/login.py>`_.

Contributing Guide
------------------

Please check the `Contributing Guide <docs/source/07_contributing.rst>`_ for details.

Core Team
---------

* `Zhiwei Zhang <https://github.com/zhiwei2017>`_ - *Author* / *Maintainer* - `zhiwei2017@gmail.com <mailto:zhiwei2017@gmail.com?subject=[GitHub]FastAPI%20Cookiecutter>`_

Literature
----------

+ `cookiecutter`_
+ `FastAPI <https://fastapi.tiangolo.com>`_
+ `Pydantic <https://pydantic-docs.helpmanual.io>`_
+ `SQLAlchemy <https://www.sqlalchemy.org>`_
+ `Alembic <https://alembic.sqlalchemy.org/en/latest/>`_
+ `PyJWT <https://github.com/jpadilla/pyjwt>`_
+ `python-jose <https://github.com/mpdavis/python-jose>`_

.. _`cookiecutter`: https://github.com/cookiecutter/cookiecutter
.. _uvicorn-gunicorn-docker: https://github.com/tiangolo/uvicorn-gunicorn-docker
