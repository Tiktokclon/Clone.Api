import os
from typing import List, Dict, Optional
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
    StoppingCriteria,
    StoppingCriteriaList
)
from app.config import settings

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = [50278, 50279, 50277, 1, 0]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

class LLMClient:
    def __init__(self):
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Charge les modèles configurés"""
        for model_name, model_config in settings.LLM_MODELS.items():
            print(f"Loading {model_name}...")
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            tokenizer = AutoTokenizer.from_pretrained(
                model_config["path"],
                use_fast=True
            )
            
            model = AutoModelForCausalLM.from_pretrained(
                model_config["path"],
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                low_cpu_mem_usage=True,
                device_map="auto"
            )
            
            self.models[model_name] = {
                "model": model,
                "tokenizer": tokenizer,
                "device": device,
                "max_length": model_config.get("max_length", 4096)
            }
    
    async def generate(
        self,
        model_name: str,
        prompt: str,
        max_tokens: int = 100,
        temperature: float = 0.7,
        top_p: float = 0.9,
        no_filters: bool = True
    ) -> str:
        """Génère du texte avec le modèle spécifié"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not loaded")
        
        model_data = self.models[model_name]
        tokenizer = model_data["tokenizer"]
        model = model_data["model"]
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model_data["device"])
        
        # Génération avec paramètres
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            stopping_criteria=StoppingCriteriaList([StopOnTokens()])
        )
        
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Post-processing si nécessaire
        if not no_filters:
            generated = apply_safety_filters(generated)
        
        return generated

llm_client = LLMClient()
