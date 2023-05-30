"""Production environment configuration."""
# mypy: ignore-errors
from ..utils.logging import ColorFormatter, StandardFormatter
from .base import Settings, LoggingConfig


class SettingsProd(Settings):
    DEBUG = False
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
                'level': "ERROR",
                'formatter': 'standardFormatter',
                'stream': 'ext://sys.stdout',
            },
        },
        "loggers": {
            "smc_crawler": {
                'handlers': ['consoleHandler'],
                'level': "ERROR",
            },
            "uvicorn": {
                'handlers': ['consoleHandler']
            },
            "uvicorn.access": {
                'handlers': []
            }
        }

    }
