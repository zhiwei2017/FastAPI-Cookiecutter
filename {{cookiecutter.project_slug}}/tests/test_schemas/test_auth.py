import pytest
from pydantic import ValidationError
from {{cookiecutter.project_slug}}.app.schemas.auth import (
    Token, AuthUserPublic, LoginForm, AuthUserCreationForm
)


def test_token_success():
    t1 = Token(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                            "eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjI0NT"
                            "YzMDAzfQ.SXuWTMZ0XvxCJN5uGt6ktQL59V5HrP"
                            "jPZYu7tr6n9GY",
               token_type="Bearer")
    assert t1.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."\
                              "eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjI0NT"\
                              "YzMDAzfQ.SXuWTMZ0XvxCJN5uGt6ktQL59V5HrP"\
                              "jPZYu7tr6n9GY"
    assert t1.token_type == "Bearer"

    t2 = Token(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                            "eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjI0NT"
                            "YzMDAzfQ.SXuWTMZ0XvxCJN5uGt6ktQL59V5HrP"
                            "jPZYu7tr6n9GY")
    assert t2.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
                              "eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjI0NT" \
                              "YzMDAzfQ.SXuWTMZ0XvxCJN5uGt6ktQL59V5HrP" \
                              "jPZYu7tr6n9GY"
    assert t2.token_type == "Bearer"


def test_token_fail():
    with pytest.raises(ValidationError):
        Token()
    with pytest.raises(ValidationError):
        Token(token_type="Bearer")


def test_user_public_success():
    up = AuthUserPublic(username="johndoe")
    assert up.username == "johndoe"
    assert up.email is None
    assert up.fullname is None
    assert up.is_active
    assert not up.is_superuser


def test_user_public_fail():
    with pytest.raises(ValidationError):
        AuthUserPublic()


def test_login_form_success():
    form = LoginForm(username="dummy", password="dummy")
    assert form.username == "dummy"
    assert form.password == "dummy"


def test_login_form_fail():
    with pytest.raises(ValidationError):
        LoginForm()
    with pytest.raises(ValidationError):
        LoginForm(username="dummy")
    with pytest.raises(ValidationError):
        LoginForm(password="dummy")


def test_user_creation_form():
    form = AuthUserCreationForm(username="dummy", password="dummy",
                                fullname=None, email=None, is_superuser=False)
    assert form.username == "dummy"
    assert form.password == "dummy"
    assert form.fullname is None
    assert form.email is None
    assert not form.is_superuser


def test_user_creation_form_fail():
    with pytest.raises(ValidationError):
        AuthUserCreationForm()
    with pytest.raises(ValidationError):
        AuthUserCreationForm(username="dummy")
    with pytest.raises(ValidationError):
        AuthUserCreationForm(password="dummy")
