from src.core.base_service import BaseService
from src.repository import MovieRepository
from src.core.exceptions import NotFoundError


class RatingService(BaseService):
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository
        super().__init__(movie_repository)

    # tag::add[]
    def add(self, user_id, movie_id, rating):
        # Create function to save the rating in the database

        record = self.movie_repository.create_rating(
            user_id=user_id, movie_id=movie_id, rating=rating)

        if record is None:
            raise NotFoundError

        return record["movie"]

    def for_movie(self, _id, sort='timestamp', order='ASC', limit=6, skip=0):
        """
        Return a paginated list of reviews for a Movie.

        Results should be ordered by the `sort` parameter, and in the direction specified
        in the `order` parameter.
        Results should be limited to the number passed as `limit`.
        The `skip` variable should be used to skip a certain number of rows.
        """
        # Get ratings for a Movie

        return self.movie_repository.get_movie_ratings(_id, sort, order,
                                                       limit, skip)
    # end::forMovie[]
