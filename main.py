from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.models import completions, chat, embeddings, images
from app.utils.auth import validate_api_key
from app.config import settings

app = FastAPI(
    title="OpenAI Unlimited API",
    description="API sans limites ni restrictions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes principales
app.include_router(
    completions.router,
    prefix="/v1/completions",
    tags=["completions"],
    dependencies=[Depends(validate_api_key)]
)

app.include_router(
    chat.router,
    prefix="/v1/chat",
    tags=["chat"],
    dependencies=[Depends(validate_api_key)]
)

app.include_router(
    embeddings.router,
    prefix="/v1/embeddings",
    tags=["embeddings"],
    dependencies=[Depends(validate_api_key)]
)

app.include_router(
    images.router,
    prefix="/v1/images",
    tags=["images"],
    dependencies=[Depends(validate_api_key)]
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "access": "unlimited",
        "restrictions": "none"
    }
