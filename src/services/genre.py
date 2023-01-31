from src.core.base_service import BaseService
from src.repository import GenresRepository


class GenreService(BaseService):
    def __init__(self, genre_repository: GenresRepository):
        self.people_repository = genre_repository
        super().__init__(genre_repository)
