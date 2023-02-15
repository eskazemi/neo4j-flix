from typing import Callable
from contextlib import AbstractContextManager
from neo4j import Session
from src.repository.base_repository import BaseRepository


class MovieRepository(BaseRepository):
    DATABASE = ""
    NODE_NAME = "Movie"

    def __init__(self, session_factory: Callable[
        ..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory)

    def all_favorites_base_user_id(self, sort, order, limit, skip, user_id):
        with self.session_factory() as session:
            # Retrieve a list of movies favorited by the user
            movies = session.execute_read(lambda tx: tx.run("""
                             MATCH (u:User {{userId: $userId}})-[r:HAS_FAVORITE]->(m:Movie)
                             RETURN m {{
                                 .*,
                                 favorite: true
                             }} AS movie
                             ORDER BY m.`{0}` {1}
                             SKIP $skip
                             LIMIT $limit
                         """.format(sort, order), userId=user_id, limit=limit,
                                                            skip=skip).value(
                "movie"))
            return movies

    def remove_from_favorites(self, user_id, movie_id):
        with self.session_factory() as session:
            # Define a transaction function to delete the HAS_FAVORITE
            # relationship within a Write Transaction
            row = session.run("""
                         MATCH (u:User {userId: $userId})-[r:HAS_FAVORITE]->(m:Movie {tmdbId: $movieId})
                         DELETE r
                         RETURN m {
                             .*,
                             favorite: false
                         } AS movie
                     """, userId=user_id, movieId=movie_id).single()
            return row

    def add_to_favorites(self, user_id, movie_id):
        with self.session_factory() as session:
            row = session.run("""
                         MATCH (u:User {userId: $userId})
                         MATCH (m:Movie {tmdbId: $movieId})
                         MERGE (u)-[r:HAS_FAVORITE]->(m)
                         ON CREATE SET u.createdAt = datetime()
                         RETURN m {
                             .*,
                             favorite: true
                         } AS movie
                     """, userId=user_id, movieId=movie_id).single()
            return row

    def create_rating(self, user_id, movie_id, rating):
        with self.session_factory() as session:
            return session.run("""
                     MATCH (u:User {userId: $user_id})
                     MATCH (m:Movie {tmdbId: $movie_id})
                     MERGE (u)-[r:RATED]->(m)
                     SET r.rating = $rating,
                         r.timestamp = timestamp()
                     RETURN m {
                         .*,
                         rating: r.rating
                     } AS movie
                     """, user_id=user_id, movie_id=movie_id,
                               rating=rating).single()

    def get_movie_ratings(self, id, sort, order, limit, skip):
        with self.session_factory() as session:
            cypher = """
                     MATCH (u:User)-[r:RATED]->(m:Movie {{tmdbId: $id}})
                     RETURN r {{
                         .rating,
                         .timestamp,
                         user: u {{
                             .userId, .name
                         }}
                     }} AS review
                     ORDER BY r.`{0}` {1}
                     SKIP $skip
                     LIMIT $limit
                     """.format(sort, order)

            result = session.run(cypher, id=id, limit=limit, skip=skip)

            return [row.get("review") for row in result]

    def get_movies_in_genre(self, sort, order, limit, skip, user_id, name):
        favorites = self.get_user_favorites(user_id)

        with self.session_factory() as session:
            cypher = """
                         MATCH (m:Movie)-[:IN_GENRE]->(:Genre {{name: $name}})
                         WHERE exists(m.`{0}`)
                         RETURN m {{
                             .*,
                             favorite: m.tmdbId in $favorites
                         }} AS movie
                         ORDER BY m.`{0}` {1}
                         SKIP $skip
                         LIMIT $limit
                     """.format(sort, order)

            result = session.run(cypher, name=name, limit=limit, skip=skip,
                                 user_id=user_id, favorites=favorites)

            return [row.get("movie") for row in result]

    def get_user_favorites(self, user_id):
        if user_id is None:
            return []
        with self.session_factory() as session:
            result = session.run("""
                MATCH (u:User {userId: $userId})-[:HAS_FAVORITE]->(m)
                RETURN m.tmdbId AS id
            """, userId=user_id)

            return [record.get("id") for record in result]
    # end::getUserFavorites[]
