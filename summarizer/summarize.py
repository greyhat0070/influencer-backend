import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL = "facebook/bart-large-cnn"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

async def summarize_text(text: str) -> str:
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 150,
            "min_length": 30,
            "do_sample": False
        }
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(HF_API_URL, headers=headers, json=payload)

        if response.status_code == 503:
            raise RuntimeError("Model is loading on Hugging Face. Please wait and try again in a few seconds.")

        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(f"Hugging Face API Error: {result['error']}")

        if not isinstance(result, list) or not result or "summary_text" not in result[0]:
            raise ValueError(f"Unexpected response format: {result}")

        return result[0]["summary_text"]
