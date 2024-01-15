from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ML API"
    model_config = SettingsConfigDict(env_file=".env")
    ACCESS_TOKEN: str
    learning_rate: float
    n_estimators: int
    max_depth: int
    loss: str


@cache
def get_settings():
    return Settings()
