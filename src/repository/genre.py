from typing import Callable
from contextlib import AbstractContextManager
from neo4j import Session
from base_repository import BaseRepository


class GenresRepository(BaseRepository):

    DATABASE = ""
    NODE_NAME = "Genre"

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory)

    def get_movies(self):
        with self.session_factory() as session:
            result = session.run("""
                       MATCH (g:Genre)
                       WHERE g.name <> '(no genres listed)'
                       CALL {
                           WITH g
                           MATCH (g)<-[:IN_GENRE]-(m:Movie)
                           WHERE m.imdbRating IS NOT NULL AND m.poster IS NOT NULL
                           RETURN m.poster AS poster
                           ORDER BY m.imdbRating DESC LIMIT 1
                       }
                       RETURN g {
                           .*,
                           movies: size((g)<-[:IN_GENRE]-(:Movie)),
                           poster: poster
                       } AS genre
                       ORDER BY g.name ASC
                   """)

            return [g.value(0) for g in result]

    def find_genre(self, name):
        with self.session_factory() as session:
            first = session.run("""
                        MATCH (g:Genre {name: $name})<-[:IN_GENRE]-(m:Movie)
                        WHERE m.imdbRating IS NOT NULL AND m.poster IS NOT NULL AND g.name <> '(no genres listed)'
                        WITH g, m
                        ORDER BY m.imdbRating DESC
                        WITH g, head(collect(m)) AS movie
                        RETURN g {
                            .name,
                            movies: size((g)<-[:IN_GENRE]-()),
                            poster: movie.poster
                        } AS genre
                    """, name=name).single()
            return first

