"""Endpoints for getting version information."""
from typing import Any
from fastapi import APIRouter
from ..schemas.base import VersionResponse
from ..version import __version__

base_router = APIRouter()


@base_router.get("/version", response_model=VersionResponse)
async def version() -> Any:
    """Provide version information about the web service.

    \f
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return VersionResponse(version=__version__)
