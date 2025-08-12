from fastapi import HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="Authorization")

async def validate_api_key(request: Request, api_key: str = Depends(api_key_header)):
    """Validate API key (in production, use a proper key management system)"""
    if settings.REQUIRE_AUTH and api_key != f"Bearer {settings.API_KEY}":
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key. Get a powerful key at our premium service."
        )
    return True
