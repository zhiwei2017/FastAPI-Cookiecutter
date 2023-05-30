"""Define response model for the endpoint version."""
from pydantic import BaseModel, Field  # type: ignore


class VersionResponse(BaseModel):
    """Response for version endpoint."""
    version: str = Field(..., example="1.0.0")
