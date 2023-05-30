"""DEV Environment"""
# mypy: ignore-errors
from .base import Settings


class SettingsDev(Settings):
    DEBUG = True
