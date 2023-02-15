from fastapi import (
    APIRouter,
    Depends
)
from src.core.container import Container
from dependency_injector.wiring import (
    Provide,
    inject
)
from src.services.movie import MovieService


movie_router = APIRouter(prefix="/movie", tags=["Movie"],)


@movie_router.get('/')
@inject
def get_movies(service: MovieService = Depends(
                    Provide[Container.movie_service])):
    pass


@movie_router.get('/<movie_id>')
@inject
def get_movie_details(movie_id, service: MovieService = Depends(
                    Provide[Container.movie_service])):
    pass


@movie_router.get('/<movie_id>/ratings')
@inject
def get_movie_ratings(movie_id, service: MovieService = Depends(
                    Provide[Container.movie_service])):
    pass


@movie_router.get('/<movie_id>/similar')
@inject
def get_similar_movies(movie_id, service: MovieService = Depends(
                    Provide[Container.movie_service])):
    pass
