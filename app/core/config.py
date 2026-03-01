from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # These names must match the keys in docker-compose.yml environment:
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    QDRANT_HOST: str = Field(default="localhost")
    QDRANT_PORT: int = 6333
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    
    # Storage settings
    STORAGE_DIR: str = "storage"

    class Config:
        env_file = ".env" # Fallback to a file if not in Docker

settings = Settings()
