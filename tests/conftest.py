import pytest
from collections import OrderedDict
from helpers.utils import generate_supported_combinations


def pytest_configure():
    """pytest hook function for configuring the global variables in tests."""
    pytest.OPTIONS = OrderedDict([
        ("license", ["MIT", "APACHE", "2-Clause BSD", "3-Clause BSD", "GPL", "None"]),
        ("use_database", ["No", "Yes"]),
        ("ci_tool", ["GitLab", "None"])
    ])
    pytest.UNSUPPORTED_COMBINATIONS = [
    ]
    pytest.SUPPORTED_COMBINATIONS = generate_supported_combinations(
        pytest.OPTIONS, pytest.UNSUPPORTED_COMBINATIONS)


@pytest.fixture
def context():
    return {
        "project_name": "My Test Project",
        "project_slug": "my_test_project",
        "project_url": "https://github.com/my_test_project",
        "author": "Test Author",
        "email": "test.author@example.com",
        "short_description": "A short description of the project.",
        "version": "0.1.0",
    }
