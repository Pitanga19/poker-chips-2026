from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Poker Chips 2026'
    PROJECT_VERSION: str = '0.1.0'
    DATABASE_URL: str

    class Config:
        env_file = '.env'

settings = Settings()
