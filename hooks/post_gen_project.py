import os
import shutil


def generate_license():
    if "{{cookiecutter.license}}" != "None":
        os.rename(os.path.join("LICENSES", "{{cookiecutter.license}}"), "LICENSE")
    shutil.rmtree("LICENSES")


def remove_dotgitlabciyml_file():
    os.remove(".gitlab-ci.yml")


def remove_github_actions():
    shutil.rmtree(".github")


def remove_bitbucket_pipeline_yml_file():
    os.remove("bitbucket-pipelines.yml")


def remove_db_files():
    shutil.rmtree("{{cookiecutter.project_slug}}/app/db")
    shutil.rmtree("tests/test_db")


def remove_auth_files():
    os.remove("{{cookiecutter.project_slug}}/app/api/auth.py")
    os.remove("{{cookiecutter.project_slug}}/app/db/models/auth.py")
    os.remove("{{cookiecutter.project_slug}}/app/schemas/auth.py")
    os.remove("{{cookiecutter.project_slug}}/app/utils/security.py")
    os.remove("{{cookiecutter.project_slug}}/app/utils/storage.py")
    os.remove("tests/test_api/test_auth.py")
    os.remove("tests/test_db/test_models/test_auth.py")
    os.remove("tests/test_schemas/test_auth.py")
    os.remove("tests/test_utils/test_security.py")
    os.remove("tests/test_utils/test_storage.py")
    os.remove("docker/init.sql")


def remove_scripts_prestart_files():
    os.remove("scripts/prestart.sh")


if __name__ == "__main__":
    generate_license()
    if "{{cookiecutter.ci_tool}}" != "GitLab":
        remove_dotgitlabciyml_file()
    if "{{cookiecutter.ci_tool}}" != "GitHub":
        remove_github_actions()
    if "{{cookiecutter.ci_tool}}" != "Bitbucket":
        remove_bitbucket_pipeline_yml_file()
    if "{{cookiecutter.use_oauth}}" == "No":
        remove_auth_files()
    if "{{cookiecutter.use_database}}" == "No":
        remove_db_files()