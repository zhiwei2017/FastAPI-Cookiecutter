import os
import pytest
import subprocess
import shutil
from helpers.utils import _fixture_id


@pytest.mark.parametrize("context_override", pytest.SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_pytest_passes(cookies, context_override):
    """Generated project should pass pytest."""
    result = cookies.bake(extra_context=context_override)
    project_path = str(result.project_path)
    current_dir = os.getcwd()
    try:
        new_env = os.environ.copy()
        if context_override["use_database"] == "Yes" and not new_env.get("SQLALCHEMY_DATABASE_URI"):
            new_env["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
        os.chdir(project_path)
        subprocess.run("python3 -m venv venv_tmp "
                       "&& source ./venv_tmp/bin/activate "
                       "&& make test && ", shell=True, env=new_env)
    except Exception as e:
        pytest.fail(str(e))
    finally:
        os.chdir(current_dir)
        shutil.rmtree(project_path)
