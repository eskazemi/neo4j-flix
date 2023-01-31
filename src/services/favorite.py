from src.core.base_service import BaseService
from src.repository import MovieRepository


class FavoriteService(BaseService):

    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository
        super().__init__(movie_repository)

