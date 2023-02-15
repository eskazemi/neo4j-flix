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
    GenreService,
    FavoriteService
)

settings = get_setting()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.core.api.genre",
            "src.core.api.movie",
            "src.core.api.account",
            "src.core.api.people",
            "src.core.api.auth",
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
    genre_repository = providers.Factory(GenresRepository,
                                         session_faqctory=db.provided.session)
    people_repository = providers.Factory(PeopleRepository,
                                          session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService,
                                     user_repository=user_repository)
    rate_service = providers.Factory(RatingService,
                                     movie_repository=MovieRepository)
    genre_service = providers.Factory(GenreService,
                                      genre_repository=genre_repository)
    movie_service = providers.Factory(MovieService,
                                      movie_repository=movie_repository)
    people_service = providers.Factory(PeopleService,
                                       people_repository=people_repository)
    user_service = providers.Factory(UserService,
                                     user_repository=user_repository)
    favorite_service = providers.Factory(FavoriteService,
                                         movie_repository=movie_repository)
