from sqlalchemy import Column, Integer, String
from {{cookiecutter.project_slug}}.app.db import Base


class DummyTable(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=True)


def test_tablename():
    assert DummyTable.__tablename__ == "dummytable"


def test_asdict():
    d = DummyTable(id=1, username="dummy username", fullname="dummy fullname")
    assert d._asdict() == dict(id=1, username="dummy username",
                               fullname="dummy fullname")
