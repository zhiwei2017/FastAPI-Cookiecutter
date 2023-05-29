# Test

## Introduction
With the tests set we're able to test multiple things:

+ `test_initialization.py`: bake project with `cookiecutter` for all possible supported choice combinations.

+ `test_linting.py`: run linting checks (**flake8**, **mypy**, **bandit**) in baked project.

+ `test_pytest.py`: run **pytest** in baked project.

+ `test_running.sh`: run the baked project and check whether the standard healthcheck and version endpoints are available.

With the help of the tests, we can guarantee the quality of every baked project using this 
template. 

## Structure

    ./tests
    ├── README.md
    ├── conftest.py                 pytest configurations. fixtures, global variables etc.
    ├── helpers                     helper functions used in tests.
    │   ├── __init__.py
    │   └── utils.py                utility functions.
    ├── test_initialization.py      test whether this template can successfully bake a project.
    ├── test_linting.py             check the lintings in baked project.
    ├── test_pytest.py              check whether the tests in baked project passed.
    └── test_running.sh             check whether the baked project can run.

## Guidelines

+ If a new prompt is added, please update the function **pytest_configure** in `conftest.py` with the new option and unsupported combinations. 

    For example, if *use_database=Yes* and *ci_tool=None* is unsupported, the **UNSUPPORTED_COMBINATIONS** will
    look like as following:
    ``` python
    pytest.UNSUPPORTED_COMBINATIONS = [{"user_db": "Yes", "ci_tool": None}]
    ```
    The value of other options besides *use_database* and *ci_tool* will be taken into account automatically.

+ If a new linting check step is added, you just need to update the `test_linting.py` file.
+ If a new standard endpoint is added, please update the `test_running.sh` file to check whether it's available when the API is online.