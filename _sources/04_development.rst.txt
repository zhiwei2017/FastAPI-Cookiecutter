.. _development-guide:

Developer Guide
===============

Project structure
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

.. _uvicorn-gunicorn-docker: https://github.com/tiangolo/uvicorn-gunicorn-docker