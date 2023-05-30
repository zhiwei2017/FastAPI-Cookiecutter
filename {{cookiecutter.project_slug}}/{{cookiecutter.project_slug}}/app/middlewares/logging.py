"""Define logging related middleware functions."""
import logging
import time
from fastapi import Request, Response
from typing import Callable
from ..configs import get_settings
from ..utils.logging import request_msg_format, get_request_msg_args

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


async def log_time(request: Request, call_next: Callable) -> Response:
    """Middleware function for logging the processing time of the request.

    It's used as an example for showing people how to define middleware
    functions and add them to the FastAPI instance.

    Args:
        request (Request): incoming request to API service.
        call_next (Callable): the corresponding endpoint function

    Returns:
        Response: a json response returned by the endpoint function.
    """
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    args = get_request_msg_args(request, response, process_time)
    logger.info(request_msg_format, *args)

    return response
