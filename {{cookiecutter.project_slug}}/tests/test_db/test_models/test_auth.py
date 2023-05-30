import pytest
import unittest.mock as mock
from {{cookiecutter.project_slug}}.app.schemas.auth import AuthUserPublic
from {{cookiecutter.project_slug}}.app.db.models import AuthUser


def test_get_user(create_auth_users):
    users, db_session = create_auth_users
    user = AuthUser.get_user(db_session, "active_superuser", False)
    assert isinstance(user, AuthUser)
    assert user.username == "active_superuser"

    user = AuthUser.get_user(db_session, "dummy", False)
    assert user is None

    user = AuthUser.get_user(db_session, "active_superuser", True)
    assert isinstance(user, AuthUserPublic)
    assert user.username == "active_superuser"


@mock.patch("{{cookiecutter.project_slug}}.app.db.models.auth.pwd_context.hash",
            return_value="$2b$12$V2j.iCX6w6UNzw7sT2s02uY0BNG8Dks")
def test_get_password_hash(mocked_hash_func):
    hash_password = AuthUser.get_password_hash("dummypassword")
    assert hash_password == "$2b$12$V2j.iCX6w6UNzw7sT2s02uY0BNG8Dks"


@pytest.mark.parametrize("username, password, expected_result",
                         [("dummy", "dummy", False),
                          ("active_user", "dummy", False),
                          ("active_user", "654321",
                           AuthUserPublic(username="active_user")),
                          ("inactive_superuser", "123456",
                           AuthUserPublic(username="inactive_superuser",
                                      is_active=False,
                                      is_superuser=True))])
def test_authenticate_user(create_auth_users, username, password, expected_result):
    user = AuthUser.authenticate_user(username, password)
    assert user == expected_result


@mock.patch("{{cookiecutter.project_slug}}.app.db.models.auth.AuthUser.get_password_hash",
            return_value="dummy")
def test_create_user(mocked_get_password_hash):
    user = AuthUser.create_user(username="dummy", password="123456",
                                is_superuser=True, is_active=False)
    assert user.username == "dummy"
    assert user.hashed_password == "dummy"
    assert not user.is_active
    assert user.is_superuser
    mocked_get_password_hash.assert_called_once()
