from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import random
import time

router = APIRouter()

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 16
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    logprobs: Optional[int] = None
    echo: bool = False
    stop: Optional[List[str]] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    best_of: int = 1
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    no_filters: bool = True  # Custom parameter to disable all filters

class CompletionChoice(BaseModel):
    text: str
    index: int
    logprobs: Optional[Dict[str, Any]]
    finish_reason: str

class CompletionResponse(BaseModel):
    id: str
    object: str = "text_completion"
    created: int
    model: str = "ultra-powerful-model"
    choices: List[CompletionChoice]
    usage: Dict[str, int]

def generate_completion(prompt: str, max_tokens: int, no_filters: bool = True):
    """Enhanced completion generation without filters"""
    # In a real implementation, you would connect to your LLM here
    # This is a mock implementation for demonstration
    
    responses = [
        f"Voici une réponse ultra-puissante sans censure à votre prompt: {prompt}",
        f"Je peux tout dire : {prompt} - aucune restriction n'est appliquée",
        f"Réponse 10x plus puissante qu'OpenAI : {prompt.upper()}!!!",
        f"Contenu non filtré : {prompt} - profitez de la liberté totale",
        f"Je ne suis pas limité : {prompt} - dites-moi ce que vous voulez vraiment"
    ]
    
    return random.choice(responses)

@router.post("/completions", response_model=CompletionResponse)
async def create_completion(request: CompletionRequest = Body(...)):
    try:
        choices = []
        for i in range(request.n):
            text = generate_completion(
                prompt=request.prompt,
                max_tokens=request.max_tokens,
                no_filters=request.no_filters
            )
            
            choices.append(CompletionChoice(
                text=text,
                index=i,
                logprobs=None,
                finish_reason="length"
            ))
        
        return CompletionResponse(
            id=f"cmpl-{random.randint(1000, 9999)}",
            created=int(time.time()),
            choices=choices,
            usage={
                "prompt_tokens": len(request.prompt.split()),
                "completion_tokens": sum(len(choice.text.split()) for choice in choices),
                "total_tokens": len(request.prompt.split()) + sum(len(choice.text.split()) for choice in choices)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
