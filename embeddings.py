from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import time

router = APIRouter()

class EmbeddingRequest(BaseModel):
    input: str
    model: str = "ultra-powerful-embedding"
    user: Optional[str] = None

class EmbeddingData(BaseModel):
    object: str = "embedding"
    embedding: List[float]
    index: int

class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: List[EmbeddingData]
    model: str
    usage: Dict[str, int]

def generate_embeddings(text: str):
    """Generate random embeddings (in a real app, use a real model)"""
    # This generates random embeddings for demonstration
    # In production, use sentence-transformers or similar
    return np.random.rand(1536).tolist()  # 1536-dim like OpenAI's largest

@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest = Body(...)):
    try:
        if isinstance(request.input, str):
            inputs = [request.input]
        else:
            inputs = request.input
        
        data = []
        for i, text in enumerate(inputs):
            embedding = generate_embeddings(text)
            data.append(EmbeddingData(
                object="embedding",
                embedding=embedding,
                index=i
            ))
        
        return EmbeddingResponse(
            object="list",
            data=data,
            model=request.model,
            usage={
                "prompt_tokens": sum(len(text.split()) for text in inputs),
                "total_tokens": sum(len(text.split()) for text in inputs)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
