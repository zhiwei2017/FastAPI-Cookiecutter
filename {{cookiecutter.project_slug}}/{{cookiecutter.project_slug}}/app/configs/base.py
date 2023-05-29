"""Base settings class contains only important fields."""
# mypy: ignore-errors
import ast
import os
import secrets
{% if cookiecutter.use_database == 'Yes' -%}
from typing import List, Union, Dict, Optional, Any
from pydantic import BaseModel, AnyHttpUrl, BaseSettings, validator, PostgresDsn
{% else -%}
from typing import List, Union, Dict
from pydantic import BaseModel, AnyHttpUrl, BaseSettings, validator
{% endif -%}
from ..utils.logging import StandardFormatter, ColorFormatter


class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool = False
    formatters: Dict
    handlers: Dict
    loggers: Dict


class Settings(BaseSettings):
    PROJECT_NAME: str = '{{cookiecutter.project_name}}'
    PROJECT_SLUG: str = '{{cookiecutter.project_slug}}'

    DEBUG: bool = True
    API_STR: str = "/api/v1"

    # ##################### Access Token Configuration #########################
    # TODO: Please note that, the secret key will be different for each running
    # instance or each time restart the service, if you prefer a stable one,
    # please use an environment variable.
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 60 minutes * 24 hours * 30 * 6  months = 6 months
    ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN: int = 60 * 24 * 30 * 6
    JWT_ENCODE_ALGORITHM: str = "HS256"

    # ########################### CORS Configuration ###########################
    """CORS_ORIGINS is a JSON-formatted list of origins
    e.g: ["http://localhost", "http://localhost:4200", "http://localhost:3000",
    "http://localhost:8080"]"""
    CORS_ORIGINS: Union[List[AnyHttpUrl], str] = []
    """A regex string to match against origins that should be permitted to make
    cross-origin requests.
    For example, your domain is example, then the regex should be something like
        ```r"https:\/\/.*\.example\.?"```
    """
    CORS_ORIGIN_REGEX: str = None
    """A list of HTTP methods that should be allowed for cross-origin requests.
    Defaults to ['*']. You can use ['GET'] to allow standard GET method."""
    CORS_METHODS: List[str] = ['GET']
    """A list of HTTP request headers that should be supported for cross-origin
    requests. Defaults to ['*'] to allow all headers. """
    CORS_HEADERS: List[str] = []
    """ Indicate that cookies should be supported for cross-origin requests.
    Defaults to True."""
    CORS_CREDENTIALS: bool = True

    # noinspection PyMethodParameters
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Validate the value of BACKEND_CORS_ORIGINS.

        Args:
            v (Union[str, List[str]): the value of BACKEND_CORS_ORIGINS.

        Returns:
            A list of urls, if v is a list of str in string format.
            The given value v, if v is a list or string.

        Raises
            ValueError, if v is in other format.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("[") and v.endswith("]"):
            return ast.literal_eval(v)
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    {% if cookiecutter.use_database == 'Yes' -%}
    # ########################### DB Configuration #############################
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    # set the default value to None, such that the assemble_db_connection can
    # build the URI for us and do checks.
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # noinspection PyMethodParameters
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Assemble the postgres DB URI with the provided POSTGRES_SERVER,
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.

        Args:
            v (Optional[str]): the value of defined SQLALCHEMY_DATABASE_URI.
            values (Dict[str, Any]): a dictionary contains the requisite values.

        Returns:
            str: the postgres DB URI.
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    {% endif -%}
    # ######################## Logging Configuration ###########################
    # logging configuration for the project logger, uvicorn loggers
    LOGGING_CONFIG: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            'colorFormatter': {'()': ColorFormatter},
            'standardFormatter': {'()': StandardFormatter},
        },
        "handlers": {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': "DEBUG",
                'formatter': 'standardFormatter',
                'stream': 'ext://sys.stdout',
            },
        },
        "loggers": {
            "{{cookiecutter.project_slug}}": {
                'handlers': ['consoleHandler'],
                'level': "DEBUG",
            },
            "uvicorn": {
                'handlers': ['consoleHandler']
            },
            "uvicorn.access": {
                # Use the project logger to replace uvicorn.access logger
                'handlers': []
            }
        }
    }

    class Config:
        case_sensitive = True
