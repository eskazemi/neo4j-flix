from src.core.base_service import BaseService
from src.repository import MovieRepository


class RatingService(BaseService):
    def __init__(self, movie_repository: MovieRepository):
        self.rating_repository = movie_repository
        super().__init__(movie_repository)
