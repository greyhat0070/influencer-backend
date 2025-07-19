import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Model version ID for ThinkSound
MODEL_VERSION = "fbe6f7b94b814be289b132d2bfa9b584d75545b6e0e66c56985a5ddc93026444"
REPLICATE_API_URL = "https://api.replicate.com/v1/predictions"

headers = {
    "Authorization": f"Token {REPLICATE_API_TOKEN}",
    "Content-Type": "application/json"
}

async def summarize_text(text: str) -> str:
    payload = {
        "version": MODEL_VERSION,
        "input": {
            "input": text
        }
    }

    async with httpx.AsyncClient() as client:
        # Step 1: Create the prediction job
        response = await client.post(REPLICATE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        prediction = response.json()
        prediction_url = prediction["urls"]["get"]

        # Step 2: Poll until status is 'succeeded'
        while True:
            poll_response = await client.get(prediction_url, headers=headers)
            poll_response.raise_for_status()
            result = poll_response.json()

            if result["status"] == "succeeded":
                return result["output"]
            elif result["status"] == "failed":
                raise RuntimeError("Summarization failed.")
            
            await asyncio.sleep(1)  # avoid hitting rate limits
