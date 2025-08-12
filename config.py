from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "ultra-powerful-secret-key"
    REQUIRE_AUTH: bool = False  # Set to True in production
    MAX_TOKENS_LIMIT: int = 100000  # 10x OpenAI's limit
    
    class Config:
        env_file = ".env"

settings = Settings()
