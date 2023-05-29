Source
======
..
    Here the source code. List here all modules.

{{cookiecutter.project_slug}}.app.api.base
{{ (( cookiecutter.project_slug | length ) + ( '.app.api.base' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.api.base
    :members:

{% if cookiecutter.use_oauth == "Yes" -%}
{{cookiecutter.project_slug}}.app.api.auth
{{ (( cookiecutter.project_slug | length ) + ( '.app.api.auth' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.api.auth
    :members:

{% endif -%}
{% if cookiecutter.use_database == "Yes" -%}
{{cookiecutter.project_slug}}.app.db.session
{{ (( cookiecutter.project_slug | length ) + ( '.app.db.session' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.db.session
    :members:

{{cookiecutter.project_slug}}.app.db.base
{{ (( cookiecutter.project_slug | length ) + ( '.app.db.base' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.db.base
    :members:

{% endif -%}
{% if cookiecutter.use_oauth == "Yes" -%}
{{cookiecutter.project_slug}}.app.db.models.auth
{{ (( cookiecutter.project_slug | length ) + ( '.app.db.models.auth' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.db.models.auth
    :members:

{% endif -%}
{{cookiecutter.project_slug}}.app.events.base
{{ (( cookiecutter.project_slug | length ) + ( '.app.events.base' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.events.base
    :members:

{{cookiecutter.project_slug}}.app.middlewares.logging
{{ (( cookiecutter.project_slug | length ) + ( '.app.middlewares.logging' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.middlewares.logging
    :members:

{{cookiecutter.project_slug}}.app.schemas.base
{{ (( cookiecutter.project_slug | length ) + ( '.app.schemas.base' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.schemas.base
    :members:

{% if cookiecutter.use_oauth == "Yes" -%}
{{cookiecutter.project_slug}}.app.schemas.auth
{{ (( cookiecutter.project_slug | length ) + ( '.app.schemas.auth' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.schemas.auth
    :members:

{% endif -%}
{{cookiecutter.project_slug}}.app.utils.logging
{{ (( cookiecutter.project_slug | length ) + ( '.app.utils.logging' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.utils.logging
    :members:

{% if cookiecutter.use_oauth == "Yes" -%}
{{cookiecutter.project_slug}}.app.utils.security
{{ (( cookiecutter.project_slug | length ) + ( '.app.utils.security' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.utils.security
    :members:

{{cookiecutter.project_slug}}.app.utils.storage
{{ (( cookiecutter.project_slug | length ) + ( '.app.utils.storage' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.utils.storage
    :members:

{% endif -%}
{{cookiecutter.project_slug}}.app.application
{{ (( cookiecutter.project_slug | length ) + ( '.app.application' | length ))  * "-" }}
.. automodule:: {{cookiecutter.project_slug}}.app.application
    :members:
