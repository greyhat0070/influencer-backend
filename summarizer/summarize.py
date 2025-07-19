import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Recommended: facebook/bart-large-cnn or google/pegasus-xsum
MODEL = "facebook/bart-large-cnn"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

async def summarize_text(text: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": text}
        )
        response.raise_for_status()

        result = response.json()
        
        # Handle possible queue state (Hugging Face sometimes queues on cold starts)
        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(f"Hugging Face API Error: {result['error']}")

        return result[0]["summary_text"]
