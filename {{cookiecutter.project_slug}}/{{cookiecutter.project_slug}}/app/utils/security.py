"""Define functions or classes related to security topic, such as token
generation, validation etc."""
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt  # type: ignore
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from ..configs import get_settings
from ..schemas.auth import AuthUserPublic
from ..db.models import AuthUser
from ..db.session import session_scope

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.API_STR + "/auth/token")
http_auth = HTTPBearer()


async def get_current_user(token: str = Depends(oauth2_scheme)) \
        -> AuthUserPublic:
    """Get the token associated user.

    Args:
        token (str): access token.

    Returns:
        AuthUserPublic: found matched user.

    Raises:
        HTTPException: if username not found, or json decode error.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token,
                             settings.SECRET_KEY,
                             algorithms=[settings.JWT_ENCODE_ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with session_scope() as session:
        user = AuthUser.get_user(session, username, populate=True)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: AuthUserPublic = Depends(get_current_user)) \
        -> AuthUserPublic:
    """Get the active user.

    Args:
        current_user (User): current user to check whether it's active.

    Returns:
        AuthUserPublic: found active user.

    Raises:
        HTTPException: if current user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    return current_user


def create_access_token(subject: Union[str, int],
                        expires_delta: Optional[timedelta] = None) -> str:
    """Create an access JSON Web Tokens.

    Args:
        subject (Union[str, Any]): subject for the token, could be use id.
        expires_delta (timedelta): the time interval of the token validity.

    Returns:
        str: created JWT.

    Examples:

        >>> from datetime import timedelta
        >>> from ..db.models import AuthUser
        >>> from ..db.session import session_scope
        >>> with session_scope() as session:
        ...     user = AuthUser.get_user(session, username, populate=True)
        >>> expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        >>> create_access_token(user.id, expires_delta=expires_delta)
    """
    if not expires_delta:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                             algorithm=settings.JWT_ENCODE_ALGORITHM)
    return encoded_jwt
