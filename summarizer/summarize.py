import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Model version ID for ThinkSound
MODEL_VERSION = "3ac27883b40c1fe7179c5fdff9dfda39d53f6e4c43a8f7006c0dbf1e5f2a75a3"
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
