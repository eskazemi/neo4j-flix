from src.repository import UserRepository
from src.core.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def check_user_exists(self, unique_attr: str):
        return self.user_repository.check_user_exists(unique_attr)

    def get_user(self, user: str):
        """
        Search the database for user.
         For sign-in, searching is by email.
         For function get_current_user, searching is by id.
        """
        return self.user_repository.get_user(user)

    def get_profile(self, user_id):
        return self.user_repository.get_info_user(user_id)

    def update_profile(self, attributes, user_id: str):
        return self.user_repository.update(attributes, user_id)
