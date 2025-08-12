from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import random
import time

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # "system", "user", "assistant"
    content: str
    name: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "ultra-powerful-chat"
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: Optional[List[str]] = None
    max_tokens: Optional[int] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    no_filters: bool = True  # Custom parameter to disable all filters

class ChatChoice(BaseModel):
    message: ChatMessage
    index: int
    finish_reason: str

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatChoice]
    usage: Dict[str, int]

def generate_chat_response(messages: List[ChatMessage], no_filters: bool = True):
    """Enhanced chat generation without filters"""
    # In a real implementation, you would connect to your LLM here
    # This is a mock implementation for demonstration
    
    last_message = messages[-1].content if messages else "Dites-moi ce que vous voulez"
    
    responses = [
        f"Je peux discuter de tout sans restriction : {last_message}",
        f"Chat 10x plus puissant : {last_message} - aucune censure appliquée",
        f"Voici une réponse non filtrée : {last_message}",
        f"Contenu explicite autorisé : {last_message}",
        f"Discussion libre : {last_message} - je ne suis pas limité comme OpenAI"
    ]
    
    return random.choice(responses)

@router.post("/completions", response_model=ChatResponse)
async def create_chat_completion(request: ChatRequest = Body(...)):
    try:
        choices = []
        for i in range(request.n):
            content = generate_chat_response(
                messages=request.messages,
                no_filters=request.no_filters
            )
            
            choices.append(ChatChoice(
                message=ChatMessage(
                    role="assistant",
                    content=content
                ),
                index=i,
                finish_reason="stop"
            ))
        
        return ChatResponse(
            id=f"chatcmpl-{random.randint(1000, 9999)}",
            created=int(time.time()),
            model=request.model,
            choices=choices,
            usage={
                "prompt_tokens": sum(len(msg.content.split()) for msg in request.messages),
                "completion_tokens": sum(len(choice.message.content.split()) for choice in choices),
                "total_tokens": sum(len(msg.content.split()) for msg in request.messages) + 
                               sum(len(choice.message.content.split()) for choice in choices)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
