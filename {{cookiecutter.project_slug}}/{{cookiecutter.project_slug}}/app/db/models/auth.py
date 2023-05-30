"""User table for authentication."""
import datetime
from typing import Union, Any
from passlib.context import CryptContext  # type: ignore
from sqlalchemy import Column, Integer, String, Boolean, DateTime  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from ..base import Base
from ..session import session_scope
from ...schemas.auth import AuthUserPublic

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUser(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=True)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True),
                        default=datetime.datetime.utcnow())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=datetime.datetime.utcnow())

    @classmethod
    def get_user(cls,
                 db_session: Session,
                 username: str,
                 populate: bool = False) -> Any:
        """Get the corresponding user with given username in DB.

        Args:
            db_session (:obj:`sqlalchemy.orm.Session`): DB session for getting
              the user corresponding given username.
            username (str): username for searching user.
            populate (bool): if True, returns a public user profile (without
              password).

        Returns:
            Union[None, AuthUserPublic]: found user or None.
        """
        user = db_session.query(cls).filter(cls.username == username).scalar()
        if not populate:
            return user
        return AuthUserPublic(**user._asdict()) if user else user

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Get hashed version of the plaintext password.

        Args:
            password (str): plaintext password.

        Returns:
            str: hashed password.
        """
        return pwd_context.hash(password)

    @classmethod
    def authenticate_user(cls,
                          username: str,
                          password: str) -> Union[bool, AuthUserPublic]:
        """Authentication the user with given username and password.

        Args:
            username (str): username of the user to check.
            password (str): password of the user to check.

        Returns:
            Union[bool, AuthUserPublic]: if user exists and password is correct, return
            found user. Otherwise, just return False.
        """
        with session_scope() as session:
            user = cls.get_user(session, username)
            if not user:
                return False
            elif not pwd_context.verify(password, user.hashed_password):
                return False
            return AuthUserPublic(**user._asdict())

    @classmethod
    def create_user(cls, username: str, password: str, **data):
        """Create a new user.

        Args:
            username (str): username of the user.
            password (str): plaintext password.
            data (dict): other user information.

        Returns:
            AuthUser: newly created user instance.
        """
        hashed_password = cls.get_password_hash(password)
        return cls(username=username,  # type: ignore
                   hashed_password=hashed_password,  # type: ignore
                   **data)  # type: ignore
