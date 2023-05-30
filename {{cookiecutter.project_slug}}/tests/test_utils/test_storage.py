import unittest.mock as mock
from {{cookiecutter.project_slug}}.app.utils.storage import store_user
from {{cookiecutter.project_slug}}.app.db.models import AuthUser
from {{cookiecutter.project_slug}}.app.schemas.auth import AuthUserPublic


def test_store_user_existent(create_auth_users):
    user_info = store_user(username="active_superuser", password="123456",
                           is_superuser=True)
    assert user_info is None


@mock.patch("{{cookiecutter.project_slug}}.app.utils.storage.logger")
def test_store_user_success(mocked_logger, create_auth_users):
    users, db_session = create_auth_users
    user_info = store_user(username="dummy_user", password="123456")
    assert user_info == AuthUserPublic(username='dummy_user', email=None,
                                       fullname=None, is_active=True,
                                       is_superuser=False)
    mocked_logger.info.assert_called_once_with('Successfully stored '
                                               'AuthUser[id="5", '
                                               'username="dummy_user"]')
    mocked_logger.error.assert_not_called()
    assert db_session.query(AuthUser).count() == 5
