import os
import pytest
import subprocess
import shutil
from helpers.utils import _fixture_id


def linting_check(cookies, linting_type, context_override, call_params=None):
    """Generated project should pass linting checks.

    Args:
        cookies (cookiecutter.cookie): cookiecutter interface for baking project.
        linting_type (str): type of linting check.
        context_override (list of dict): overriede the default context.
        call_params (list of str): extra parameters for calling linting check.

    Returns:

    """
    result = cookies.bake(extra_context=context_override)
    project_path = str(result.project_path)
    if call_params is None:
        call_params = ["--config", "setup.cfg"]
    call_params.append(result.context['project_slug'])
    call_params = " ".join(call_params)
    current_dir = os.getcwd()
    try:
        os.chdir(project_path)
        subprocess.run("python3 -m venv venv_tmp "
                       "&& source ./venv_tmp/bin/activate "
                       "&& pip install -r ./requirements/dev.txt "
                       f"&& {linting_type} {call_params}",
                       shell=True)
    except Exception as e:
        pytest.fail(str(e))
    finally:
        os.chdir(current_dir)
        shutil.rmtree(project_path)


@pytest.mark.parametrize("context_override", pytest.SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_flake8_passes(cookies, context_override):
    """Generated project should pass flake8."""
    linting_check(cookies, "flake8", context_override)


@pytest.mark.parametrize("context_override", pytest.SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_mypy_passes(cookies, context_override):
    """Generated project should pass mypy."""
    linting_check(cookies, "mypy", context_override)


@pytest.mark.parametrize("context_override", pytest.SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_bandit_passes(cookies, context_override):
    """Generated project should pass bandit."""
    linting_check(cookies, "bandit", context_override, call_params=['-r'])
