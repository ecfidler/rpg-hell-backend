from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    discord_client_id: str
    discord_client_secret: str
    discord_redirect_uri: str
    database_host: str
    database_user: str
    database_password: str
    database_name: str
    jwt_secret: str
    mode: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings():
    return Settings()
