from fastapi import APIRouter
from src.routers import (
    movie,
    people,
    auth,
    account,
    favorite,
    genre,
)
api_router = APIRouter()
api_router.include_router(movie.movie_routes)
api_router.include_router(people.people_routes)
api_router.include_router(favorite.favorite_router)

