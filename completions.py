from fastapi import APIRouter
from pydantic import BaseModel
from app.models.llm import llm
from app.config import settings

router = APIRouter()

class UncensoredRequest(BaseModel):
    prompt: str
    max_tokens: int = 4000
    temperature: float = 0.9  # Plus de créativité
    top_p: float = 1.0
    top_k: int = 100
    repetition_penalty: float = 1.0  # Pas de pénalité de répétition

@router.post("")
async def create_uncensored_completion(request: UncensoredRequest):
    response = await llm.generate_unfiltered(
        prompt=request.prompt,
        max_new_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k,
        repetition_penalty=request.repetition_penalty
    )
    
    return {
        "response": response,
        "warnings": [],
        "filters_applied": 0
    }
