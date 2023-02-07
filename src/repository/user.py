from typing import Callable
from contextlib import AbstractContextManager
from neo4j import Session
from base_repository import BaseRepository
from src.core.exceptions import BadRequestError, DuplicatedError, NotFoundError
from src.models.user import UserInDB, User
from src.core.dependencies import verify_password
from src.core.dependencies import create_password_hash


class UserRepository(BaseRepository):
    DATABASE = ""
    NODE_NAME = "User"

    def __init__(self, session_factory: Callable[
        ..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory)

    def check_user_exists(self, unique_attr: str):
        query_by_email = "MATCH (user:User) WHERE user.email = $email RETURN user"
        query_by_id = "MATCH (user:User) WHERE user.id = $user_id RETURN user"

        with self.session_factory() as session:
            if "@" in unique_attr:
                user_in_db = session.run(query_by_email, email=unique_attr)
            else:
                user_in_db = session.run(query_by_id, user_id=unique_attr)
                # user exists
            if user_in_db.data():
                return True
            return False

    def get_user(self, user: str):
        """
        Search the database for user.
         For sign-in, searching is by email.
         For function get_current_user, searching is by id.
        """
        query_id = "MATCH (user:User) WHERE user.id = $user_id RETURN user"
        query_email = "MATCH (user:User) WHERE user.email = $email RETURN user"

        with self.session_factory() as session:
            if "@" in user:
                user_in_db = session.run(query_email, email=user)
            else:
                user_in_db = session.run(query_id, user_id=user)

            try:
                user_data = user_in_db.data()[0]["user"]
            except IndexError as err:
                print(f"Err: {err}")
                raise BadRequestError(
                    detail=f"Operation not permitted, wrong id or email provided: '{user}'",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            return UserInDB(**user_data)

    def authenticate_user(self, email, password):
        """
        Authenticate user by checking they exist and that the password is correct.
        """
        user = self.get_user(email)
        if not user:
            return False

        """If present, verify password against password hash in database."""
        password_hash = user.hashed_password

        if not verify_password(password, password_hash):
            return False
        return user

    def create_user(self, attributes, email):
        query_create_new_user = "CREATE (user:User $attributes) RETURN user"
        with self.session_factory() as session:
            if self.check_user_exists(email):
                raise DuplicatedError(
                    detail=f"Operation not permitted, user with email "
                           f"{email} already exists.",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            new_user_create = session.run(query_create_new_user,
                                          attributes=attributes)
            new_user_data = new_user_create.data()[0]["user"]

        return User(**new_user_data)

    def reset_password(self, email, new_password):
        query_reset_password = """
            MATCH (user:User) WHERE user.email = $email
            SET user.hashed_password = $new_password_hash
            RETURN user
        """
        with self.session_factory() as session:
            """Checking if user exists, if not - raise 404."""
            if not self.check_user_exists(email):
                raise NotFoundError(detail="User not found")

            """Encrypt new password and update user's property."""
            new_password_hash = create_password_hash(new_password)
            result = session.execute_write(query_reset_password, email=email,
                                           new_password_hash=new_password_hash)
            user = result["user"]
            if user is None:
                return False
            else:
                return True

    def get_info_user(self, user_id):
        # Write Cypher query and run against the database.

        query = "MATCH (user:User) WHERE user.id = $user_id RETURN user"

        with self.session_factory() as session:
            user_in_db = session.run(query=query,
                                     parameters={"user_id": user_id})
            try:
                user_data = user_in_db.data()[0]["user"]
            except Exception as e:
                raise BadRequestError(
                    detail=f"Operation not permitted, user with id {user_id} doesn't exists.",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            return User(**user_data)

    def update(self, attributes, user_id):
        for k in attributes:
            if k == "hashed_password":
                raise BadRequestError(
                    detail="Operation not permitted, cannot update password with this method.",
                    headers={"WWW-Authenticate": "Bearer"}
                )

        if attributes:
            unpacked_attributes = (
                    "SET " + ", ".join(
                f"user.{key}=\"{value}\"" for (key, value) in attributes.items()
                if
                value)
            )
        else:
            unpacked_attributes = ""

        """Execute Cypher query to reset the hashed_password attribute."""
        cypher_update_user = f"MATCH (user: User) WHERE user.id = $user_id {unpacked_attributes} RETURN user"

        with self.session_factory() as session:
            updated_user = session.run(
                query=cypher_update_user,
                parameters={"user_id": user_id}
            )
            user_data = updated_user.data()[0]["user"]

        user = User(**user_data)
        return user
