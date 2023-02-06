from src.core.container import Container
from dependency_injector.wiring import (
    Provide,
    inject
)
from fastapi import Query
from src.services.favorite import FavoriteService
from src.services.rating import RatingService
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
def get_favorites(user_id: str,
                  skip: int = 0,
                  limit: int = 10,
                  order: str = 'ASK',
                  sort: str = 'title',
                  service: FavoriteService = Depends(
                      Provide[Container.auth_service])):
    # Get search parameters

    output = service.all(user_id, sort, order, limit, skip)
    return output

    # return jsonify(output)


@account_routes.post('/favorites/<movie_id>')
@inject
def add_favorite(movie_id, user_id, service: FavoriteService = Depends(
    Provide[Container.auth_service])):
    # Get user ID from JWT
    # user_id = current_user["sub"]

    output = service.add(user_id, movie_id)
    return output
    # Return the output
    # return jsonify(output)


@account_routes.delete('/favorites/<movie_id>')
@inject
def delete_favorite(movie_id, user_id, service: FavoriteService = Depends(
    Provide[Container.auth_service])):
    # Get user ID from JWT
    # user_id = current_user["sub"]

    output = service.remove(user_id, movie_id)
    return output
    # Return the output
    # return jsonify(output)


@account_routes.post('/ratings/<movie_id>')
@inject
def save_rating(movie_id, rating: int = Query(...), service: RatingService = Depends(
    Provide[Container.auth_service])):
    # Get user ID from JWT
    # user_id = current_user["sub"]

    # Save the rating
    output = service.add(user_id, movie_id, rating)

    # Return the output
    return output
    # return jsonify(output)

