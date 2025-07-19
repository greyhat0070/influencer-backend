from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from fetchers.youtube_fetcher import fetch_youtube_videos
from summarizer.summarize import summarize_text
from database.supabase_client import insert_summary

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Influencer Monitoring Agent is running"}

# Pydantic Models
class SummarizeRequest(BaseModel):
    text: str

class SaveRequest(BaseModel):
    platform: str
    handle: str
    content: str
    summary: str

# Fetch and summarize YouTube content
@app.get("/fetch/youtube")
async def fetch_youtube(handle: str):
    videos = await fetch_youtube_videos(handle)
    full_text = " ".join([v["title"] + " " + v["description"] for v in videos])
    summary = await summarize_text(full_text)
    await insert_summary(
        platform="YouTube",
        handle=handle,
        content=full_text,
        summary=summary
    )
    return {"summary": summary}

# Summarize any input text
@app.post("/summarize/")
async def summarize_endpoint(data: SummarizeRequest):
    summary = await summarize_text(data.text)
    return {"summary": summary}

# Save pre-summarized data manually
@app.post("/save/")
async def save_summary(data: SaveRequest):
    await insert_summary(
        platform=data.platform,
        handle=data.handle,
        content=data.content,
        summary=data.summary
    )
    return {"status": "saved"}

# For Render/Fly.io
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
