"""OAuth2 authentication related endpoints."""
from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from ..db.models import AuthUser
from ..schemas.auth import (
    Token, AuthUserPublic, AuthUserCreationForm, LoginForm
)
from ..utils.security import (
    create_access_token, get_current_active_user, http_auth
)
from ..utils.storage import store_user
from ..configs import get_settings

settings = get_settings()
auth_router = APIRouter()


@auth_router.post("/token", response_model=Token)
async def login(form_data: LoginForm = Depends()) -> Token:
    """Login with credentials to get access token.

    \f

    Args:
        form_data (:obj:`LoginForm`): contains username and password.

    Returns:
        :obj:`Token`: create access token.

    Raises:
        :obj:`HTTPException`: if not authenticated user, or user is inactive.
    """
    user = AuthUser.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    elif user.is_superuser:  # type: ignore
        expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN
    else:
        expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=expire_minutes)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires  # type: ignore
    )
    return Token(access_token=access_token, token_type="Bearer")  # nosec


@auth_router.post("/user/new",
                  response_model=AuthUserPublic,
                  dependencies=[Depends(http_auth)])
async def create_user(current_active_user: AuthUserPublic = Depends(get_current_active_user),
                      form_data: AuthUserCreationForm = Depends()) -> AuthUserPublic:
    """Create a new user through a superuser.

    \f

    Args:
        current_active_user (AuthUserPublic): from token extracted current
          activate user.
        form_data (UserCreationForm): form data containing new user's
          credentials and information.

    Returns:
        AuthUserPublic: a brief of newly created user.
    """
    if not current_active_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied.")
    try:
        user = store_user(**form_data.dict())
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to store in DB.")
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists.")
    return user


@auth_router.get("/user/info",
                 response_model=AuthUserPublic,
                 dependencies=[Depends(http_auth)])
async def get_user_info(
        current_user: AuthUserPublic = Depends(get_current_active_user)) \
        -> AuthUserPublic:
    """Use the access token to get the current user's account information.

    \f

    Args:
        current_user (:obj:`..schemas.auth.User`): the corresponding user of the
          pass token.

    Returns:
        :obj:`..schemas.auth.User`: the corresponding user of the
          pass token.
    """
    return current_user
