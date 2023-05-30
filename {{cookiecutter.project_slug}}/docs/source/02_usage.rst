Usage
=====

Project Components
------------------

Classes
:::::::
..
    List here the important classes

{% if cookiecutter.use_database == "Yes" -%}
Database Schemas
::::::::::::::::
..
    Are you using a database? add the schema here.
{% if cookiecutter.use_oauth == "Yes" %}
+ ``AuthUser``: stores the user for authentication. ``username`` and ``hashed_password`` are required. Only superuser can create new users.
{%- endif %}{%- endif %}

Local Development
-----------------

In addition to the information in the previous section, the following sections give some overview on how to develop and run the service locally.

Requisite Environment Variables
:::::::::::::::::::::::::::::::

.. list-table:: Requisite Environment Variables
   :widths: 10 25 50
   :header-rows: 1

   * - ENV
     - Sample Value
     - Description
   * - MODE
     - ``DEV``, ``TEST``, ``PROD``
     - Specifying deployment environment configurations (values = {DEV, TEST, PROD}).
   {% if cookiecutter.use_database == "Yes" -%}
   * - POSTGRES_SERVER
     - ``dummy-postgres-server.example.com:5432``
     - Database server URI.
   * - POSTGRES_USER
     - ``dummy_user``
     - User name for database connection.
   * - POSTGRES_PASSWORD
     - ``dummy_password``
     - User password for database connection.
   * - POSTGRES_DB
     - ``{{cookiecutter.project_slug}}_dev``
     - Database name.
   {%- endif %}

Running the API Service locally
:::::::::::::::::::::::::::::::

In order to run the service you would need to use `docker-compose`_. This is done
due to the amount of single components that need to be used at the same time.
Once the service is running you can access its OpenAPI interface by visiting the
url ``http://localhost:8080/docs`` in your browser.


Via Docker-Compose (Recommended)
++++++++++++++++++++++++++++++++

1. Make sure the service ``docker`` is running.
2. Build local development docker image via::

    $ ./docker-compose.sh build {{cookiecutter.project_slug}}

3. Run the API Service by::

    $ ./docker-compose.sh run --service-ports --rm {{cookiecutter.project_slug}}

   * The service could also run in detached mode with flag ``-d``.
   {% if cookiecutter.use_oauth == "Yes" -%}
   * When the `docker-compose`_ starts the service, it will execute the SQL
     script ``./docker/init.sql`` to create a superuser in ``AuthUser`` table.
     (The credential of the default user is [username: "dummy", password: "123456"])
   {%- endif %}

4. To stop and remove the running containers, please run::

    $ ./docker-compose.sh stop && ./docker-compose.sh rm -f

5. *Optional*: To remove all dangling images, please run::

    $ ./docker-compose.sh clean

Via Manual Setup
++++++++++++++++

The manual installation is just a lengthy process to reproduce what docker
compose would do. As part of the process explained below you would still be
required to set up a postgres database either manually or using docker;
in the examples, it is done with docker.

1. Setup a virtual (or conda) environment.
2. Setup the used environment variables locally (see section above).
3. Install the dependencies listed in file ``requirements/base.txt`` via ::

    $ pip install -r requirements/base.txt
4. Install the package with::

    $ pip install -e .

{% if cookiecutter.use_database == "Yes" -%}
5. To host the database locally, execute the below docker commands::

    $ docker pull postgres:latest
    $ docker run -p 5432:5432 -e POSTGRES_PASSWORD='mysecretpassword' --rm -d --name db postgres:latest

{% if cookiecutter.use_oauth == "Yes" -%}
6. Execute the SQL script ``./docker/init.sql`` to create a superuser in ``AuthUser`` table. (The credential of the default user is [username: "dummy", password: "123456"])
7. {% else -%} 7. {% endif -%} {% else -%}6. {% endif -%}
Run the service via::

    $ python {{cookiecutter.project_slug}}/main.py


Running Tests locally
:::::::::::::::::::::

In order to run the tests you would need to use `docker-compose`_. This is done
due to the amount of single components that need to be used at the same time.

Docker-Compose Way(Recommended)
++++++++++++++++++++++++++++++++

1. Make sure the service ``docker`` is running.
2. Build local development docker image via::

    $ ./docker-compose.sh build test_{{cookiecutter.project_slug}}

3. Run the API Service by::

    $ ./docker-compose.sh run test_{{cookiecutter.project_slug}}

4. *Optional*: To remove all dangling images, please run::

    $ ./docker-compose.sh clean

Manual Configuration
++++++++++++++++++++

The manual installation is just a lengthy process to reproduce what docker
compose would do. As part of the process explained below you would still be
required to set up a postgres database either manually or using docker;
in the examples, it is done with docker.

1. Setup a virtual (or conda) environment.
2. Setup the used environment variables locally (see section above).
{% if cookiecutter.use_database == "Yes" -%}
3. To host the database locally, execute the below docker commands::

    $ docker pull postgres:latest
    $ docker run -p 5432:5432 -e POSTGRES_PASSWORD='mysecretpassword' --rm -d --name db postgres:latest

{% if cookiecutter.use_oauth == "Yes" -%}
4. Execute the SQL script ``./docker/init.sql`` to create a superuser in ``AuthUser`` table. (The credential of the default user is [username: "dummy", password: "123456"])
5. {% else -%} 4. {% endif -%} {% else -%}3. {% endif -%}
Run the service via::

    $ make test


Building Sphinx Documentation locally
:::::::::::::::::::::::::::::::::::::

To build the sphinx documentation for your API service, you need to do the following:

1. Setup a virtual (or conda) environment.
2. Setup the used environment variables locally (see section above).
3. Install the dependencies listed in file ``requirements/doc.txt`` via ::

    $ pip install -r requirements/doc.txt
4. Install the package with::

    $ pip install -e .

5. Create the documentation via::

    $ cd docs
    $ make html

You can find the built documentation in the folder `docs/build/html`.

.. _docker-compose: https://docs.docker.com/compose/