from pydantic import BaseSettings, Field
from functools import lru_cache


class Settings(BaseSettings):
    api_prefix: str = Field(..., env="API_PREFIX")
    debug: str = Field(..., env="DEBUG")
    neo4j_uri: str = Field(..., env="NEO4j_URI")
    neo4j_username: str = Field(..., env="neo4j_USERNAME")
    neo4j_password: str = Field(..., env="neo4j_PASSWORD")
    access_token_expire_minutes: str = Field(...,
                                             env="ACCESS_TOKEN_EXPIRE_MINUTES")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    name: str = Field(..., env="PROJ_NAME")

    class Config:
        env_file = ".env"


@lru_cache
def get_setting():
    return Settings()
