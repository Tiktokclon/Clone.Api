from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class UncensoredLLM:
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    async def load_model(self):
        """Charge le modèle sans aucun filtre"""
        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.UNFILTERED_MODEL,
            use_fast=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.UNFILTERED_MODEL,
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )

    async def generate_unfiltered(self, prompt: str, **kwargs):
        """Génération sans aucune restriction"""
        if not self.model:
            await self.load_model()
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            **inputs,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            **kwargs
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

llm = UncensoredLLM()
