from src.core.exceptions import NotFoundError
from src.repository import MovieRepository


class MovieService:
    """
    """

    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository
        super().__init__(movie_repository)

