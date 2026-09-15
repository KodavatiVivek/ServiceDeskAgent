from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rag_service_url: str = "http://rag-service:8002/internal/rag/search"
    tool_service_url: str = "http://tool-service:8003/internal/tools/execute"
    audit_service_url: str = "http://audit-service:8005/internal/audit/events"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
