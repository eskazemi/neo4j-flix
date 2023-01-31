from src.repository import UserRepository
from src.core.base_service import BaseService
from src.core.dependencies import verify_password
from src.core.exceptions import BadRequestError
from src.models.user import UserInDB



class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    @classmethod
    def check_user_exists(cls, unique_attr: str):
        query_by_email = "MATCH (user:User) WHERE user.email = $email RETURN user"
        query_by_id = "MATCH (user:User) WHERE user.id = $user_id RETURN user"

        with neo4j_driver.session() as session:
            if "@" in unique_attr:
                user_in_db = session.run(query_by_email, email=unique_attr)
            else:
                user_in_db = session.run(query_by_id, user_id=unique_attr)
                # user exists
            if user_in_db.data():
                return True
            return False

    @classmethod
    def get_user(cls, user: str):
        """
        Search the database for user.
         For sign-in, searching is by email.
         For function get_current_user, searching is by id.
        """
        query_id = "MATCH (user:User) WHERE user.id = $user_id RETURN user"
        query_email = "MATCH (user:User) WHERE user.email = $email RETURN user"

        with neo4j_driver.session() as session:
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

    @classmethod
    def authenticate_user(cls, email, password):
        """
        Authenticate user by checking they exist and that the password is correct.
        """
        user = cls.get_user(email)
        if not user:
            return False

        """If present, verify password against password hash in database."""
        password_hash = user.hashed_password

        if not verify_password(password, password_hash):
            return False
        return user
