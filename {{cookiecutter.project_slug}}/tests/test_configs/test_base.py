import pytest
from pydantic.error_wrappers import ValidationError
from {{cookiecutter.project_slug}}.app.configs.base import Settings
from {{cookiecutter.project_slug}}.app.configs import get_settings


@pytest.mark.parametrize("mode, settings_cls",
                         [("DEV", Settings),
                          ("TEST", Settings),
                          ("PROD", Settings),
                          (None, Settings),
                          ("None", Settings)])
def test_get_settings(monkeypatch, mode, settings_cls):
    get_settings.cache_clear()
    if mode:
        monkeypatch.setenv("MODE", mode)
    settings = get_settings()
    # assert the settings is an instance of the corresponding settings class
    assert isinstance(settings, settings_cls)
    if mode:
        monkeypatch.delenv("MODE")


@pytest.mark.parametrize("cors_origins, expected_result",
                         [(["https://example.com", "https://example.de"],
                           ["https://example.com", "https://example.de"]),
                          ("https://example.com, https://example.de",
                           ["https://example.com", "https://example.de"]),
                          ("['https://example.com', 'https://example.de']",
                           ["https://example.com", "https://example.de"])
                          ])
def test_assemble_cors_origins_success(cors_origins, expected_result):
    s = Settings(CORS_ORIGINS=cors_origins,
                 CORS_ORIGIN_REGEX='https:\\/\\/.*\\.example\\.?')
    assert s.CORS_ORIGINS == expected_result


def test_assemble_cors_origins_fail():
    with pytest.raises(ValueError) as e:
        Settings(CORS_ORIGINS=None)
    assert type(e.value) == ValidationError
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0] == dict(loc=('CORS_ORIGINS',),
                                       msg='None',
                                       type='value_error')

{% if cookiecutter.use_database == "Yes" -%}
def test_assemble_db_connection():
    s = Settings(SQLALCHEMY_DATABASE_URI=None, POSTGRES_USER="postgres", POSTGRES_PASSWORD="mysecretpassword",
                 POSTGRES_SERVER="localhost:5555", POSTGRES_DB="postgres")
    assert s.SQLALCHEMY_DATABASE_URI == "postgresql://postgres:mysecretpassword@localhost:5555/postgres"


def test_assemble_db_connection_with_uri():
    s = Settings(SQLALCHEMY_DATABASE_URI="postgresql://dummy:dummy@localhost:9999/dummydb",
                 POSTGRES_USER="postgres", POSTGRES_PASSWORD="mysecretpassword",
                 POSTGRES_SERVER="localhost:5555", POSTGRES_DB="postgres")
    assert s.SQLALCHEMY_DATABASE_URI == "postgresql://dummy:dummy@localhost:9999/dummydb"


def test_assemble_db_connection_fail():
    with pytest.raises(ValueError) as e:
        Settings(SQLALCHEMY_DATABASE_URI="http://dummy:dummy@localhost:9999/dummydb")
    assert type(e.value) == ValidationError
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0] == dict(ctx={'allowed_schemes': {'postgresql',
                                                                'postgres',
                                                                'postgresql+asyncpg',
                                                                'postgresql+pg8000',
                                                                'postgresql+psycopg',
                                                                'postgresql+psycopg2',
                                                                'postgresql+psycopg2cffi',
                                                                'postgresql+py-postgresql',
                                                                'postgresql+pygresql'
                                                                }},
                                       loc=('SQLALCHEMY_DATABASE_URI',),
                                       msg='URL scheme not permitted',
                                       type='value_error.url.scheme')

    with pytest.raises(ValueError) as e:
        Settings(SQLALCHEMY_DATABASE_URI=None)
    assert type(e.value) == ValidationError
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0] == dict(loc=('SQLALCHEMY_DATABASE_URI',),
                                       msg='can only concatenate str (not "NoneType") to str',
                                       type='type_error')

{% endif -%}