from src.core.container import Container
from dependency_injector.wiring import (
    Provide,
    inject
)
from src.services.favorite import FavoriteService
from src.services.rate import RatingService
from fastapi import (
    APIRouter,
    Depends,
)

account_routes = APIRouter(
    prefix="/account",
    tags=["account"],
)


@account_routes.get('/favorites')
@inject
def get_favorites(service: FavoriteService = Depends(
    Provide[Container.auth_service])):
    pass


@account_routes.post('/favorites/<movie_id>')
@inject
def add_favorite(movie_id, service: FavoriteService = Depends(
    Provide[Container.auth_service])):
    pass


@account_routes.delete('/favorites/<movie_id>')
@inject
def delete_favorite(movie_id, service: FavoriteService = Depends(
    Provide[Container.auth_service])):
    pass


@account_routes.post('/ratings/<movie_id>')
@inject
def save_rating(movie_id, service: RatingService = Depends(
    Provide[Container.auth_service])):
    pass
