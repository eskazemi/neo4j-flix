from datetime import timedelta
from src.config import get_setting
from src.core.exceptions import (
    AuthError,
    BadRequestError,
    DuplicatedError,
    NotFoundError
)
import uuid
from datetime import datetime
from src.core.security import create_access_token
from src.core.dependencies import create_password_hash
from email_validator import (
    validate_email,
    EmailNotValidError,
)
from src.services import UserService
from src.repository import UserRepository
from src.models.user import (
    User,
    UserSignIn,
    UserSignInResponse,
    UserSignUp,
    UserResetPassword,
)
from src.core.base_service import BaseService

setting = get_setting()


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def sign_in(self, user: UserSignIn):
        user = UserService.authenticate_user(user.email, user.password)
        if not user:
            raise AuthError(
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(
            minutes=setting.access_token_expire_minutes)
        access_token = create_access_token(
            subject={"sub": user.id, "email": user.email},
            expires_delta=access_token_expires
        )
        login_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "expired_in": setting.access_token_expire_minutes,
            "user_id": user.id
        }

        return UserSignInResponse(**login_data)

    async def sign_up(self, new_user: UserSignUp):
        try:
            valid = validate_email(new_user.email)
            """Update with the normalized form."""
            email = valid.email
        except EmailNotValidError:
            raise BadRequestError(
                detail=f"Operation not permitted, wrong email address provided: "
                       f"{new_user.email}",
                headers={"WWW-Authenticate": "Bearer"}
            )

        attributes = {
            "id": str(uuid.uuid4()),
            "email": email,
            "hashed_password": create_password_hash(new_user.password),
            "joined": str(datetime.utcnow()),
            "is_active": True
        }

        new_user = dict(new_user)
        del new_user["email"]
        del new_user["password"]
        attributes.update(new_user)

        query_create_new_user = "CREATE (user:User $attributes) RETURN user"
        with neo4j_driver.session() as session:
            if UserService.check_user_exists(email):
                raise DuplicatedError(
                    detail=f"Operation not permitted, user with email "
                           f"{email} already exists.",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            new_user_create = session.run(query_create_new_user,
                                          attributes=attributes)
            new_user_data = new_user_create.data()[0]["user"]

        return User(**new_user_data)

    async def reset_password(self, user_reset_pass: UserResetPassword):
        """Reset User's password using user's email."""

        email, new_password = user_reset_pass.email, user_reset_pass.new_password
        try:
            valid = validate_email(email)
            """Update with the normalized form."""
            email = valid.email
        except EmailNotValidError:
            raise BadRequestError(
                detail=f"Not valid email address was provided: '{email}'"
            )

        query_reset_password = """
            MATCH (user:User) WHERE user.email = $email
            SET user.hashed_password = $new_password_hash
            RETURN user
        """
        with neo4j_driver.session() as session:
            """Checking if user exists, if not - raise 404."""
            if not UserService.check_user_exists(email):
                raise NotFoundError(detail="User not found")

            """Encrypt new password and update user's property."""
            new_password_hash = create_password_hash(new_password)
            session.run(query_reset_password, email=email,
                        new_password_hash=new_password_hash)

        return {"detail": "Password successfully updated"}
