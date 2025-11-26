from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Poker Chips 2026'
    PROJECT_VERSION: str = '0.1.0'
    DATABASE_URL_ASYNC: str
    DATABASE_URL_SYNC: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int
    JWT_TIMEZONE: str

    class Config:
        env_file = '.env'

settings = Settings()
