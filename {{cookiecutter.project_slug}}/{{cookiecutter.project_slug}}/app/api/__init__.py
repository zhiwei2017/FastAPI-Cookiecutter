"""The main APIRouter is defined to include all the sub routers from each
module inside the API folder"""
from fastapi import APIRouter
from .base import base_router
{% if cookiecutter.use_oauth == "Yes" -%}
from .auth import auth_router
{% endif -%}
# TODO: import your modules here.

api_router = APIRouter()
api_router.include_router(base_router, tags=["base"])
{% if cookiecutter.use_oauth == "Yes" -%}
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
{% endif -%}
# TODO: include the routers from other modules
