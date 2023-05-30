Project Generation Options
==========================

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