import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PREFIX: str
    DEBUG: str
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    access_token_expire_minutes: str
    secret_key: str
    algorithm: str


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
basic_env_file, local_env_file = ".env", ".env.local"
local_env_file_path = os.path.join(project_root, local_env_file)
is_local_env_file_exist = os.path.isfile(local_env_file_path)
env_file = local_env_file if is_local_env_file_exist else basic_env_file

NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
print(NEO4J_USERNAME)
# print(basic_env_file)
# print(env_file)
# settings = Settings(
#     _env_file=env_file,
#     _env_file_encoding="utf-8"
# )
# print(settings)
