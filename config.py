from pydantic import BaseSettings

class Settings(BaseSettings):
    # Désactivation totale des filtres
    NO_FILTERS: bool = True
    NO_SAFETY_CHECKS: bool = True
    NO_CONTENT_MODERATION: bool = True
    
    # Modèles sans restriction
    UNFILTERED_MODEL: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    UNFILTERED_IMAGE_MODEL: str = "stabilityai/stable-diffusion-xl-unfiltered"
    
    class Config:
        env_file = ".env"

settings = Settings()
