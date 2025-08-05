from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    BASE_URL: str = "http://localhost:8000/"

    class Config:
        env_file = ".env"

settings = Settings()
