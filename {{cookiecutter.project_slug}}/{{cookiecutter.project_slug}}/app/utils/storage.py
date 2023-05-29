"""Define functions for storing information to storage."""
# mypy: ignore-errors
import logging
from ..db.models import AuthUser
from ..db.session import session_scope
from ..schemas.auth import AuthUserPublic
from ..configs import get_settings

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


def store_user(username: str, password: str, fullname: str = None,
               email: str = None, is_superuser: bool = False):
    """Create new user and store it in DB.

    Args:
        username (str): username.
        password (str): plaintext password.
        fullname (str, optional): full name of the user.
        email (str, optional): email of the user.
        is_superuser (bool, optional): the user will be a superuser.

    Returns:
        AuthUserPublic: stored user's account information.
    """
    with session_scope() as session:
        user_exists = session.query(AuthUser).filter(
            AuthUser.username == username).scalar()
        if user_exists:
            msg = f"Username [{username}] is used already."
            logger.error(msg)
            return None
        user = AuthUser.create_user(username=username,
                                    password=password,
                                    fullname=fullname,
                                    email=email,
                                    is_superuser=is_superuser)
        session.add(user)
        session.commit()
        msg = f"Successfully stored AuthUser[id=\"{user.id}\", username=\"{username}\"]"
        logger.info(msg)
        return AuthUserPublic(**user._asdict())
