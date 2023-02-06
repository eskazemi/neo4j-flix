from src.core.base_service import BaseService
from src.repository import MovieRepository
from src.core.exceptions import NotFoundError


class FavoriteService(BaseService):

    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository
        super().__init__(movie_repository)

    # tag::all[]
    def all(self, user_id, sort='title', order='ASC', limit=6, skip=0):
        """
        This method should retrieve a list of movies that have an incoming :HAS_FAVORITE
        relationship from a User node with the supplied `userId`.

        Results should be ordered by the `sort` parameter, and in the direction specified
        in the `order` parameter.

        Results should be limited to the number passed as `limit`.
        The `skip` variable should be used to skip a certain number of rows.
        """
        # Open a new session
        # Retrieve a list of movies favorited by the user
        return self.movie_repository.all_favorites_base_user_id(
            user_id, sort, order, limit, skip
        )

    # tag::add[]
    def add(self, user_id, movie_id):
        # Define a new transaction function to create a HAS_FAVORITE
        # relationship
        row = self.movie_repository.add_to_favorites(user_id, movie_id)
        # If no rows are returnedm throw a NotFoundException
        if row is None:
            raise NotFoundError

        return row.get("movie")

        # end::add[]

    # tag::remove[]
    def remove(self, user_id, movie_id):
        """
        This method should remove the `:HAS_FAVORITE` relationship between
        the User and Movie ID nodes provided.

        If either the user, movie or the relationship between them cannot be found,
        a `NotFoundError` should be thrown.

        """
        row = self.movie_repository.remove_from_favorites(user_id, movie_id)
        # If no rows are returnedm throw a NotFoundError
        if row is None:
            raise NotFoundError

        return row.get("movie")
