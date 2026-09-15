from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    vector_backend: str = "local-memory"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
