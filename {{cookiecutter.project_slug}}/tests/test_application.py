import unittest.mock as mock
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from {{cookiecutter.project_slug}}.app.application import create_application
from {{cookiecutter.project_slug}}.app.configs import Settings


def test_create_application():
    app = create_application()
    assert isinstance(app, FastAPI)


@mock.patch("{{cookiecutter.project_slug}}.app.application.get_settings")
def test_create_application_with_cors_origins(mocked_get_settings):
    mocked_get_settings.return_value = Settings(CORS_ORIGINS="https://example.com, https://example.de")
    app = create_application()
    assert isinstance(app, FastAPI)
    for m in app.user_middleware:
        if isinstance(m, CORSMiddleware):
            assert m.options == {'allow_origins': ['https://example.com', 'https://example.de'],
                                 'allow_origin_regex': 'https:\\/\\/.*\\.example\\.?',
                                 'allow_credentials': True,
                                 'allow_methods': ['GET'],
                                 'allow_headers': []}
