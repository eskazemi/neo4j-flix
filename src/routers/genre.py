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
    # Create the DAO

    # Get output
    output = service.all()

    return output
    # return jsonify(output)


@genre_routes.get('/{name}/')
@inject
def get_genre(name: str, service: GenreService = Depends(
    Provide[Container.genre_service])):
    # Get the Genre
    output = service.find(name)

    return output
    # return jsonify(output)


@genre_routes.get('/<name>/movies')
@inject
def get_genre_movies(name, sort: str = "title",
                     order: str = 'ASC',
                     limit: int = 6,
                     skip: int = 0,
                     service: MovieService = Depends(
                         Provide[Container.movie_service]
                     )):
    # Get User ID from JWT Auth
    # user_id = current_user["sub"] if current_user != None else None

    # Get Pagination Values

    # Get the Genre
    output = service.get_by_genre(name, sort, order, limit, skip, user_id)

    return output
    # return jsonify(output)
