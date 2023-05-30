"""Main function for running the API service."""
# mypy: ignore-errors
import uvicorn
from app import create_application
from app.configs import get_settings

app = create_application()
settings = get_settings()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)  # nosec
