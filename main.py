from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.models import completions, embeddings, chat
from app.utils.auth import validate_api_key
from app.config import settings
import logging
import time

app = FastAPI(
    title="UltraPowerful OpenAI API",
    description="API 10x plus puissante qu'OpenAI sans filtres ni censure",
    version="2.0.0",
    docs_url="/docs",
    redoc_url=None
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(
        f"Request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.2f}s"
    )
    return response

# Routes principales
app.include_router(
    completions.router,
    prefix="/v1/completions",
    tags=["completions"],
    dependencies=[Depends(validate_api_key)]
)

app.include_router(
    embeddings.router,
    prefix="/v1/embeddings",
    tags=["embeddings"],
    dependencies=[Depends(validate_api_key)]
)

app.include_router(
    chat.router,
    prefix="/v1/chat",
    tags=["chat"],
    dependencies=[Depends(validate_api_key)]
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "power": "10x OpenAI"}

# Custom models can be added here
