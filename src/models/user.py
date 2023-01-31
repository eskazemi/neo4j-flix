from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: Optional[str] = None


class User(UserUpdate):
    id: str
    email: str
    is_active: bool
    joined: datetime


class UserInDB(User):
    hashed_password: str


class UserSignIn(BaseModel):
    email: str
    password: str


class UserSignInResponse(BaseModel):
    access_token: str
    token_type: str
    expired_in: int
    user_id: str


class UserSignUp(UserSignIn):
    name: str


class UserResetPassword(BaseModel):
    email: str
    new_password: str


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str