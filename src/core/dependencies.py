from datetime import datetime, timedelta
from typing import Optional
from src.core.security import (
    ALGORITHM,
    JWTBearer
)
from dependency_injector.wiring import (
    Provide,
    inject
)
from src.core.container import Container
from fastapi import Depends
from src.user.service import UserService
from src.core.exceptions import AuthError
from passlib.context import CryptContext
from jose import (
    jwt,
    JWTError,
)

from src.config import get_setting
from src.user.models import User

settings = get_setting()

SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

"""Generate password hash."""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)


# ----------------------------------------main ---------------------------


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@inject
async def get_current_user(token: str = Depends(JWTBearer()),
                           service: UserService = Depends(
                               Provide[Container.user_service])
                           ):
    """Decrypt the token and retrieve the user."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AuthError(detail="Could not validate credentials")
    except JWTError:
        raise AuthError(detail="Could not validate credentials")
    current_user = service.get_user(user=user_id)
    if current_user is None:
        raise AuthError(detail="User not found")
    return current_user


async def get_current_active_user(
        current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    if not current_user.is_superuser:
        raise AuthError("It's not a super user")
    return current_user

