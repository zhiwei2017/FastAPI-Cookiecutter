"""Test environment configuration."""
# mypy: ignore-errors
from ..utils.logging import ColorFormatter
from .base import Settings, LoggingConfig


class SettingsTest(Settings):
    DEBUG = False
    LOGGING_CONFIG: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            'colorFormatter': {'()': ColorFormatter},
        },
        "handlers": {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': "INFO",
                'formatter': 'colorFormatter',
                'stream': 'ext://sys.stdout',
            },
        },
        "loggers": {
            "smc_crawler": {
                'handlers': ['consoleHandler'],
                'level': "INFO",
            },
            "uvicorn": {
                'handlers': ['consoleHandler']
            },
            "uvicorn.access": {
                'handlers': []
            }
        }
    }
