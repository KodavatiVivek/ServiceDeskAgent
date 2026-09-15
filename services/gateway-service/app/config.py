from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    orchestrator_url: str = "http://orchestrator-service:8001/internal/orchestrate"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
