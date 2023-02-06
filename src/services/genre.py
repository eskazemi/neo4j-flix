from src.core.base_service import BaseService
from src.repository import GenresRepository
from src.core.exceptions import NotFoundError


class GenreService(BaseService):
    def __init__(self, genre_repository: GenresRepository):
        self.genre_repository = genre_repository
        super().__init__(genre_repository)

    # tag::all[]
    def all(self):
        # Define a unit of work to Get a list of Genres

        # Execute within a Read Transaction
        return self.genre_repository.get_movies()

    # tag::find[]
    def find(self, name):
        """
         This method should find a Genre node by its name and return a set of properties
         along with a `poster` image and `movies` count.
         If the genre is not found, a NotFoundError should be thrown.
         """
        # Define a unit of work to find the genre by it's name
        first = self.genre_repository.find_genre(name)
        # If no records are found raise a NotFoundException
        if first is None:
            raise NotFoundError

        return first.get("genre")

    # end::find[]
