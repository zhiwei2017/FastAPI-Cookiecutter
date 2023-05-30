from __future__ import print_function


def validate_project_slug():
    project_slug = "{{ cookiecutter.project_slug }}"
    if hasattr(project_slug, "isidentifier"):
        assert (project_slug.isidentifier()), f"'{project_slug}' project slug is not a valid Python identifier."

    assert (project_slug == project_slug.lower()), f"'{project_slug}' project slug should be all lowercase"


def validate_author():
    assert ("\\" not in "{{ cookiecutter.author }}"), "Don't include backslashes in author."


def auth_db_handle():
    if "{{ cookiecutter.use_oauth }}" == "Yes" and "{{ cookiecutter.use_database }}" == "No":
        raise ValueError("Invalid Choice Combination: OAuth needs to use db.")


if __name__ == "__main__":
    validate_project_slug()
    validate_author()
    auth_db_handle()
