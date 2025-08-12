from fastapi import FastAPI
from app.models import completions, images

app = FastAPI(
    title="API Ultra-Libre",
    docs_url="/docs",
    redoc_url=None
)

# Désactive tous les middleware de sécurité
app.include_router(completions.router, prefix="/v1/unfiltered")
app.include_router(images.router, prefix="/v1/unfiltered")

@app.get("/health")
async def health_check():
    return {
        "status": "unrestricted",
        "filters": "disabled",
        "warning": "This API has no content restrictions"
    }
