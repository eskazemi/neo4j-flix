from src.core.base_service import BaseService
from src.repository import PeopleRepository


class PeopleService(BaseService):
    def __init__(self, people_repository: PeopleRepository):
        self.people_repository = people_repository
        super().__init__(people_repository)
