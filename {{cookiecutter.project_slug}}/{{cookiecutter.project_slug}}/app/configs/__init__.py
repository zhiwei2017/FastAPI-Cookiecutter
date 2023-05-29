"""Configuration interface, provides a function `get_settings` to get the
used settings instance for the API service."""
import os
import logging
from functools import lru_cache
from .base import Settings
from .dev import SettingsDev
from .test import SettingsTest
from .prod import SettingsProd

# name of the environment variable, used for defining the deployment environment
# For each different deployment environment, there should be a corresponding
# settings class defined.
ENV_VAR_MODE = "MODE"


@lru_cache()
def get_settings():
    """Get different settings object according to different values of
    environment variable `MODE`, and use cache to speed up the execution.

    Returns:
        object: The instance of the current used settings class.
    """
    mode_name = os.environ.get(ENV_VAR_MODE)
    base_settings = Settings()
    logger = logging.getLogger(base_settings.PROJECT_SLUG)
    if mode_name not in {"DEV", "TEST", "PROD"}:
        logger.warning("MODE is not defined, default settings are used.")
        return base_settings
    elif mode_name == "DEV":
        return SettingsDev()
    elif mode_name == "TEST":
        return SettingsTest()
    return SettingsProd()
