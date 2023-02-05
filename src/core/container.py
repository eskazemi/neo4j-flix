from dependency_injector import containers, providers
from src.config import get_setting
from src.core.provider.neo import Neo4jConnection
from src.repository import (
    MovieRepository,
    PeopleRepository,
    UserRepository,
    GenresRepository,
)
from src.services import (
    MovieService,
    AuthService,
    RatingService,
    UserService,
    PeopleService,
    GenreService
)

settings = get_setting()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.core.genre.router",
            "src.core.movie.router",
            "src.core.rating.router",
            "src.core.user.router",
            "src.core.auth.router",
            "src.core.dependencies",
        ]
    )

    db = providers.Singleton(Neo4jConnection,
                             db_url=settings.neo4j_uri,
                             uri=settings.neo4j_username,
                             pwd=settings.neo4j_password
                             )

    movie_repository = providers.Factory(MovieRepository,
                                         session_factory=db.provided.session)
    user_repository = providers.Factory(UserRepository,
                                        session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService,
                                     user_repository=user_repository)
    rate_service = providers.Factory(RatingService,
                                     movie_repository=MovieRepository)
    genre_service = providers.Factory(GenreService)
    movie_service = providers.Factory(MovieService,
                                      movie_repository=movie_repository)
    people_service = providers.Factory(PeopleService)
    user_service = providers.Factory(UserService,
                                     user_repository=user_repository)
