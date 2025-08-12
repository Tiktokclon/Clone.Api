from pydantic import BaseSettings
from typing import Dict, Any

class Settings(BaseSettings):
    # Authentification
    API_KEY: str = "ultra-powerful-secret-key"
    REQUIRE_AUTH: bool = True
    ADMIN_KEY: str = "admin-super-secret"
    
    # Billing
    BILLING_ENABLED: bool = True
    DEFAULT_PLAN: str = "free"
    
    # Modèles LLM
    LLM_MODELS: Dict[str, Dict[str, Any]] = {
        "ultra-powerful": {
            "path": "mistralai/Mistral-7B-v0.1",
            "max_length": 8192
        },
        "fast-chat": {
            "path": "facebook/opt-1.3b",
            "max_length": 2048
        }
    }
    
    # Database
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "openai_premium"
    
    # Monitoring
    START_TIME: float = 0.0  # Será configuré au démarrage
    
    class Config:
        env_file = ".env"

settings = Settings()
settings.START_TIME = time.time()
