import pytest
import unittest.mock as mock
from fastapi import status
from {{cookiecutter.project_slug}}.app.utils.security import create_access_token


@pytest.mark.parametrize("data, expected_access_token",
                         [(dict(username="active_superuser", password="123456"),
                           "active_superuser 180 days, 0:00:00"),
                          (dict(username="active_user", password="654321"),
                           "active_user 8 days, 0:00:00")])
@mock.patch("{{cookiecutter.project_slug}}.app.api.auth.create_access_token",
            side_effect=lambda subject, expires_delta: f"{subject} {expires_delta}")
def test_login_success(mocked_create_access_token, test_client,
                       create_auth_users, data, expected_access_token):
    response = test_client.post("/api/v1/auth/token", data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] == expected_access_token


@pytest.mark.parametrize("data, expected_status_code, expected_detail",
                         [(dict(username="dummy", password="dummy"), status.HTTP_401_UNAUTHORIZED,
                           "Incorrect username or password"),
                          (dict(username="inactive_user", password="654321"), status.HTTP_403_FORBIDDEN,
                           "Inactive user")])
def test_login_fail(test_client, create_auth_users, data, expected_status_code,
                    expected_detail):
    response = test_client.post("/api/v1/auth/token", data=data)
    assert response.status_code == expected_status_code
    assert response.json()["detail"] == expected_detail


@pytest.mark.parametrize("data, expected_status_code, expected_user_info",
                         [(dict(username="dummy", fullname=None,
                                password="dummy", email=None,
                                is_superuser=False),
                           status.HTTP_200_OK,
                           dict(username="dummy", is_superuser=False,
                                email=None, fullname=None, is_active=True))])
def test_create_user_success(test_client, create_auth_users, data,
                             expected_status_code, expected_user_info):
    token = create_access_token("active_superuser")
    response = test_client.post("/api/v1/auth/user/new", data=data,
                                headers={"Authorization": "Bearer "+token})
    assert response.status_code == expected_status_code
    assert response.json() == expected_user_info


@pytest.mark.parametrize("username, data, expected_status_code,"
                         " expected_detail",
                         [("active_user",
                           dict(username="dummy", fullname=None,
                                password="dummy", email=None,
                                is_superuser=False),
                           status.HTTP_403_FORBIDDEN, "Permission denied."),
                          ("active_superuser",
                           dict(username="dummy", fullname=None,
                                password="dummy", email=None,
                                is_superuser=False),
                           status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to store in DB.")])
@mock.patch("{{cookiecutter.project_slug}}.app.api.auth.store_user",
            side_effect=Exception("dummy"))
def test_create_user_fail(mocked_store_user, test_client, create_auth_users,
                          username, data, expected_status_code, expected_detail):
    token = create_access_token(username)
    response = test_client.post("/api/v1/auth/user/new", data=data,
                                headers={"Authorization": "Bearer "+token})
    assert response.status_code == expected_status_code
    assert response.json()["detail"] == expected_detail


@pytest.mark.parametrize("username, data, expected_status_code,"
                         " expected_detail",
                         [("active_superuser",
                           dict(username="active_user", fullname=None,
                                password="dummy", email=None,
                                is_superuser=False),
                           status.HTTP_409_CONFLICT, "Username already exists.")])
def test_create_user_fail_duplicate_username(test_client, create_auth_users,
                                             username, data,
                                             expected_status_code,
                                             expected_detail):
    token = create_access_token(username)
    response = test_client.post("/api/v1/auth/user/new", data=data,
                                headers={"Authorization": "Bearer " + token})
    assert response.status_code == expected_status_code
    assert response.json()["detail"] == expected_detail


def test_get_user_info(test_client, create_auth_users):
    token = create_access_token("active_user")
    response = test_client.get("/api/v1/auth/user/info",
                               headers={"Authorization": "Bearer " + token})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == dict(username="active_user", is_superuser=False,
                                   email=None, fullname=None, is_active=True)
