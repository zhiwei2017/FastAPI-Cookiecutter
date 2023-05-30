import pytest
import unittest.mock as mock
from datetime import timedelta, datetime
from fastapi import HTTPException, status
from jose import JWTError
from {{cookiecutter.project_slug}}.app.utils.security import (
    create_access_token, get_current_user, get_current_active_user
)


@pytest.mark.parametrize("user_type", ["active_user", "active_superuser",
                                       "inactive_user", "inactive_superuser"])
@pytest.mark.asyncio
async def test_get_current_user_success(create_auth_users, user_type):
    users, db_session = create_auth_users
    token = create_access_token(users[user_type].username)
    user = await get_current_user(token)
    assert user.username == users[user_type].username


@pytest.mark.asyncio
@mock.patch("{{cookiecutter.project_slug}}.app.utils.security.jwt.decode",
            return_value=dict(sub=""))
async def test_get_current_user_fail_no_username(mocked_decode, create_auth_users):
    users, db_session = create_auth_users
    token = create_access_token(users["active_user"].username)
    with pytest.raises(HTTPException) as e:
        await get_current_user(token)
    assert e.type == HTTPException
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Could not validate credentials"
    assert e.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.asyncio
@mock.patch("{{cookiecutter.project_slug}}.app.utils.security.jwt.decode",
            side_effect=JWTError())
async def test_get_current_user_fail_jwterror(mocked_decode, create_auth_users):
    users, db_session = create_auth_users
    token = create_access_token(users["active_user"].username)
    with pytest.raises(HTTPException) as e:
        await get_current_user(token)
    assert e.type == HTTPException
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Could not validate credentials"
    assert e.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.asyncio
@mock.patch("{{cookiecutter.project_slug}}.app.utils.security.AuthUser.get_user")
async def test_get_current_user_fail_no_user(mocked_get_user, create_auth_users):
    mocked_get_user.return_value = None
    users, db_session = create_auth_users
    token = create_access_token(users["active_user"].username)
    with pytest.raises(HTTPException) as e:
        await get_current_user(token)
    assert e.type == HTTPException
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Could not validate credentials"
    assert e.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.parametrize("user_type", ["active_user", "active_superuser"])
@pytest.mark.asyncio
async def test_get_current_active_user_success(create_auth_users, user_type):
    users, db_session = create_auth_users
    user = await get_current_active_user(users[user_type])
    assert user.is_active


@pytest.mark.asyncio
async def test_get_current_active_user_fail(create_auth_users):
    users, db_session = create_auth_users
    with pytest.raises(HTTPException) as e:
        await get_current_active_user(users["inactive_user"])
    assert e.type == HTTPException
    assert e.value.status_code == status.HTTP_403_FORBIDDEN
    assert e.value.detail == "Inactive user"


@pytest.mark.parametrize(
    "subject, expires_delta, expected_jwt_1, expected_jwt_2",
    [("hello", timedelta(minutes=1000),
      'eyJleHAiOjE2MDQ2NDI1MzAsInN1YiI6ImhlbGxvIn0',
      "MoGXYq3J4B5I8kHF1emAi-O3E_7jyJHr6ZiTZes_FM8"),
     ("hello", None,
      'eyJleHAiOjE2MDQ1OTQ1MzAsInN1YiI6ImhlbGxvIn0',
      "6i2sII8y9AoTh2HYQazQ5eMqd8FxT0kVwkaX659jiig"),
     (None, timedelta(minutes=1000),
      'eyJleHAiOjE2MDQ2NDI1MzAsInN1YiI6Ik5vbmUifQ',
      "UzUp3tygRtKB9AJOYejzdDSoeN5lXuOsrA3mKa76lJ0"),
     (None, None,
      'eyJleHAiOjE2MDQ1OTQ1MzAsInN1YiI6Ik5vbmUifQ',
      "un0wcIugoLh9d_Q5kdAItqVa7-hne30xKFFdbPx5Q8w"),
     (11, timedelta(minutes=1000),
      'eyJleHAiOjE2MDQ2NDI1MzAsInN1YiI6IjExIn0',
      "Ldqb90pgaMp3KpxuhMRKGCMw5BtAS2oMIdCrr44qa20"),
     (11, None,
      'eyJleHAiOjE2MDQ1OTQ1MzAsInN1YiI6IjExIn0',
      "Z8uxHltP81eXL_BYuV3B00gPHoW6NSSUe8C-T_uXlTo"),
     (1.1, timedelta(minutes=1000),
      'eyJleHAiOjE2MDQ2NDI1MzAsInN1YiI6IjEuMSJ9',
      "02DfS35n2UB4fAa1qIVZEO5RAgGOzSpkmbo6A3TuBxE"),
     (1.1, None,
      'eyJleHAiOjE2MDQ1OTQ1MzAsInN1YiI6IjEuMSJ9',
      "MHZXAO-x2tM291Izb-Cg0fVElSbxia6CThZqKNDToMc"),
     ([1, 2, 3], timedelta(minutes=1000),
      'eyJleHAiOjE2MDQ2NDI1MzAsInN1YiI6IlsxLCAyLCAzXSJ9',
      "Mgzt1K3MapxzfK-iw_xYx1nh9HFe-RCIhlGdxNSizvo"),
     ([1, 2, 3], None,
      'eyJleHAiOjE2MDQ1OTQ1MzAsInN1YiI6IlsxLCAyLCAzXSJ9',
      "2eZq4yJNCE_hURorQJRD0Hv9WN9U8Iq5tffqjDFxiRQ"),
     ({1, 2, 3}, timedelta(minutes=1000),
      'eyJleHAiOjE2MDQ2NDI1MzAsInN1YiI6InsxLCAyLCAzfSJ9',
      "K3DEdfo0FVE9zUYxBaZTK0Dd3Sno0RFajwqIqtsjCuY"),
     ({1, 2, 3}, None, 'eyJleHAiOjE2MDQ1OTQ1MzAsInN1YiI6InsxLCAyLCAzfSJ9',
      "ayQIMF_YlOX_yzmIyus33vwUz8xOtB7Iu6k1w9qNmVk"),
     ({1: '1', 2: '2', 3: '3'}, timedelta(minutes=1000),
      'eyJleHAiOjE2MDQ2NDI1MzAsInN1YiI6InsxOiAnMScsIDI6ICcyJywgMzogJzMnfSJ9',
      "hmYWs6eKqFfS4EaS6IsDp6or-IsbmezRqkCRkRNjxys"),
     ({1: '1', 2: '2', 3: '3'}, None,
      'eyJleHAiOjE2MDQ1OTQ1MzAsInN1YiI6InsxOiAnMScsIDI6ICcyJywgMzogJzMnfSJ9',
      "sjEz3oEuD38Ut7Cw9_mbmut1KexuawlJWwQ1TnX4st0")])
@mock.patch("{{cookiecutter.project_slug}}.app.utils.security.datetime")
@mock.patch("{{cookiecutter.project_slug}}.app.utils.security.settings")
def test_create_access_token(mock_settings, mocked_datetime, subject,
                             expires_delta, expected_jwt_1, expected_jwt_2):
    mock_settings.SECRET_KEY = 'EswZK2i7zI0ubzWBGpKCt68P9zWg419opysg36GP0xo'
    mock_settings.JWT_ENCODE_ALGORITHM = "HS256"
    mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 200
    mocked_datetime.utcnow.return_value = datetime(2020, 11, 5, 13, 22, 10,
                                                   516244)
    encoded_jwt = create_access_token(subject, expires_delta)
    jwt_list = encoded_jwt.split(".")
    assert len(jwt_list) == 3
    assert jwt_list[0] == 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    assert jwt_list[1] == expected_jwt_1
    assert jwt_list[2] == expected_jwt_2
    mocked_datetime.utcnow.assert_called_once()
