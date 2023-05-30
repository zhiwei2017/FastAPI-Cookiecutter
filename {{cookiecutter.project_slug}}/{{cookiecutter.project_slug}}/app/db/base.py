"""Define the base sqlalchemy model class."""
# mypy: ignore-errors
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import inspect


@as_declarative()
class Base:
    """Base table class"""
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically"""
        return cls.__name__.lower()

    def _asdict(self):
        """Convert extract record to dict."""
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
