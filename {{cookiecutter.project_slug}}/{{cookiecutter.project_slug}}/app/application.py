"""Module containing FastAPI instance related functions and classes."""
# mypy: ignore-errors
import logging.config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
{% if cookiecutter.use_oauth == "Yes" -%}
from typing import Callable
from .api.auth import login, create_user
{% endif -%}
from .api import api_router
from .configs import get_settings
{% if cookiecutter.use_database == "Yes" -%}
from .db import Base, engine
{% endif -%}
from .events import startup_handler, shutdown_handler
from .middlewares import log_time
from .version import __version__


{% if cookiecutter.use_database == "Yes" -%}
def create_db_tables():
    """Create all tables in database."""
    Base.metadata.create_all(engine)


{% endif -%}
{% if cookiecutter.use_oauth == "Yes" -%}
def update_schema_name(app: FastAPI, function: Callable, name: str) -> None:
    """
    Updates the Pydantic schema name for a FastAPI function that takes
    in a fastapi.UploadFile = File(...) or bytes = File(...).

    This is a known issue that was reported on FastAPI#1442 in which
    the schema for file upload routes were auto-generated with no
    customization options. This renames the auto-generated schema to
    something more useful and clear.

    Args:
        app (FastAPI): The FastAPI application to modify.
        function (Callable): The function object to modify.
        name (str): The new name of the schema.
    """
    for route in app.routes:
        if route.endpoint is function:
            route.body_field.type_.__name__ = name
            break


{% endif -%}
def create_application() -> FastAPI:
    """Create a FastAPI instance.

    Returns:
        object of FastAPI: the fastapi application instance.
    """
    settings = get_settings()
    application = FastAPI(title=settings.PROJECT_NAME,
                          debug=settings.DEBUG,
                          version=__version__,
                          openapi_url=f"{settings.API_STR}/openapi.json")

    # Set all CORS enabled origins
    if settings.CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in
                           settings.CORS_ORIGINS],
            allow_origin_regex=settings.CORS_ORIGIN_REGEX,
            allow_credentials=settings.CORS_CREDENTIALS,
            allow_methods=settings.CORS_METHODS,
            allow_headers=settings.CORS_HEADERS,
        )

    # add defined routers
    application.include_router(api_router, prefix=settings.API_STR)

    # event handler
    application.add_event_handler("startup", startup_handler)
    application.add_event_handler("shutdown", shutdown_handler)

    # load logging config
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    # add defined middleware functions
    application.add_middleware(BaseHTTPMiddleware, dispatch=log_time)

    {% if cookiecutter.use_oauth == "Yes" -%}
    # update schema name to avoid automatically generated name from openapi
    update_schema_name(application, login, "LoginForm")
    update_schema_name(application, create_user, "AuthUserCreationForm")

    {% endif -%}
    {% if cookiecutter.use_database == "Yes" -%}
    # create tables in db
    create_db_tables()

    {% endif -%}
    return application
