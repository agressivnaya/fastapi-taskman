"""
app/config.py: Конфигурация приложения.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "supersecretkey"
    algo: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
