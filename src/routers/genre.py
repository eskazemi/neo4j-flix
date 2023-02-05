from src.core.container import Container
from src.services.genre import GenreService
from src.services.movie import MovieService
from dependency_injector.wiring import (
    Provide,
    inject
)
from fastapi import (
    APIRouter,
    Depends,
)

genre_routes = APIRouter(
    prefix="/genre",
    tags=["genre"],
)


@genre_routes.get('/')
@inject
def get_index(service: GenreService = Depends(
    Provide[Container.genre_service])):
    pass


@genre_routes.get('/{name}/')
@inject
def get_genre(name: str, service: GenreService = Depends(
    Provide[Container.genre_service])):

    # Get the Genre
    pass


@genre_routes.get('/<name>/movies')
@inject
def get_genre_movies(name, service: MovieService = Depends(
    Provide[Container.movie_service]
)):
    # Get User ID from JWT Auth
    # user_id = current_user["sub"] if current_user != None else None

    # Get Pagination Values
    # sort = request.args.get("sort", "title")
    # order = request.args.get("order", "ASC")
    # limit = request.args.get("limit", 6, type=int)
    # skip = request.args.get("skip", 0, type=int)


    # Get the Genre
    pass

