from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_username: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str
    jwt_secret_key: str
  

@lru_cache
def get_settings():
    return Settings()