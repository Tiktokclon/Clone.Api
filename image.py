from diffusers import StableDiffusionXLPipeline
import torch
from fastapi import APIRouter
import base64
from io import BytesIO

router = APIRouter()

pipeline = None

async def get_unfiltered_pipeline():
    global pipeline
    if not pipeline:
        pipeline = StableDiffusionXLPipeline.from_pretrained(
            settings.UNFILTERED_IMAGE_MODEL,
            torch_dtype=torch.float16,
            variant="fp16",
            safety_checker=None,  # Désactive le safety checker
            requires_safety_checker=False
        ).to("cuda")
    return pipeline

@router.post("/unfiltered")
async def generate_unfiltered_image(prompt: str):
    pipe = await get_unfiltered_pipeline()
    image = pipe(prompt, num_inference_steps=50).images[0]
    
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return {
        "image": base64.b64encode(buffered.getvalue()).decode("utf-8"),
        "nsfw": True,  # Toujours considéré comme NSFW car non filtré
        "censored": False
    }
