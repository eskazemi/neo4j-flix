from src.core.exceptions import NotFoundError
from src.repository import MovieRepository


class MovieService:
    """
    """

    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository
        super().__init__(movie_repository)

    """
      This method should return a paginated list of movies that have a relationship to the
      supplied Genre.
      Results should be ordered by the `sort` parameter, and in the direction specified
      in the `order` parameter.
      Results should be limited to the number passed as `limit`.
      The `skip` variable should be used to skip a certain number of rows.
      If a user_id value is suppled, a `favorite` boolean property should be returned to
      signify whether the user has added the movie to their "My Favorites" list.
      """

    # tag::getByGenre[]
    def get_by_genre(self, name, sort='title', order='ASC', limit=6, skip=0,
                     user_id=None):
        # Get Movies in a Genre


        with self.driver.session() as session:
            return session.execute_read(get_movies_in_genre, sort, order,
                                        limit=limit, skip=skip, user_id=user_id)
    # end::getByGenre[]


