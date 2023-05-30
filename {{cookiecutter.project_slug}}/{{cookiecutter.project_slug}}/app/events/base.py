"""Define the start up events and shut down events.

Please be aware that you can define multiple events and add them to the FastAPI
instance, and the adding order decides the executing order.
"""
import logging
from ..configs import get_settings

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


async def startup_handler() -> None:
    """Dummy startup event, it will be executed before the app is ready, such
    as loading ml model, creating superuser in DB etc."""
    logger.info("Starting up ...")


async def shutdown_handler() -> None:
    """Dummy shutdown event, it will be executed before the app is shutting
    down, such as removing temporary files, close DB connection etc."""
    logger.info("Shutting down ...")
