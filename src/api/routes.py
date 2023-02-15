from fastapi import APIRouter
from src.api import (
    movie,
    people,
    auth,
    account,
    genre,
)
api_router = APIRouter()
api_router.include_router(movie.movie_routes)
api_router.include_router(people.people_routes)
api_router.include_router(auth.auth_router)
api_router.include_router(account.account_router)
api_router.include_router(genre.genre_router)

