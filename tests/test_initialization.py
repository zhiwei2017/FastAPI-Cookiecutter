import os
import re
import pytest
import yaml
from cookiecutter.exceptions import FailedHookException
from binaryornot.check import is_binary
from helpers.utils import _fixture_id

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths(paths):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        for line in open(path, "r"):
            match = RE_OBJ.search(line)
            assert match is None, f"cookiecutter variable not replaced in {path}"


@pytest.mark.parametrize("context_override", pytest.SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_project_generation(cookies, context, context_override):
    """Test that project is generated and fully rendered."""
    result = cookies.bake(extra_context={**context, **context_override})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.mark.parametrize("stage, expected_test_script",
                         [("linting:flake8", ["make ${LINTING_PKG}"]),
                          ("linting:mypy", ["make ${LINTING_PKG}"]),
                          ("linting:bandit", ["make ${LINTING_PKG}"]),
                          ("test", ["make test"])])
def test_gitlab_invokes_linting_and_pytest(cookies, context, stage,
                                           expected_test_script):
    """Test linting stage and test stage content in .gitlab-ci.yml file."""
    context.update({"ci_tool": "GitLab"})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    with open(f"{result.project}/.gitlab-ci.yml", "r") as gitlab_yml:
        try:
            gitlab_config = yaml.safe_load(gitlab_yml)
            assert gitlab_config[stage]["script"] == expected_test_script
        except yaml.YAMLError as e:
            pytest.fail(e)


@pytest.mark.parametrize("slug", ["project slug", "Project_Slug"])
def test_invalid_slug(cookies, context, slug):
    """Invalid slug should failed pre-generation hook."""
    context.update({"project_slug": slug})

    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)


@pytest.mark.parametrize("invalid_context", pytest.UNSUPPORTED_COMBINATIONS)
def test_error_if_incompatible(cookies, context, invalid_context):
    """It should not generate project an incompatible combination is selected."""
    context.update(invalid_context)
    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)
