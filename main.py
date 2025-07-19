from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn
from summarizer.summarize import summarize_text
from fetchers.youtube_fetcher import fetch_youtube_videos
from database.supabase_client import insert_summary

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for POST /summarize/
class SummarizeRequest(BaseModel):
    platform: str
    handle:str

@app.post("/summarize/")
async def summarize(request: SummarizeRequest):
    platform = request.platform
    handle = request.handle
    # Replace with real summarization logic
    return {"summary": f"Monitoring summary for {platform} handle: {handle}"}
# Route: POST /summarize/
# @app.post("/summarize/")
# async def summarize_endpoint(data: SummarizeRequest):
#     try:
#         summary = await summarize_text(data.text)
#         return {"summary": summary}
#     except Exception as e:
#         return {"error": str(e)}

# Route: GET /fetch/youtube?handle=nasdaily
@app.get("/fetch/youtube")
async def fetch_youtube(handle: str):
    try:
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
    except Exception as e:
        return {"error": str(e)}


# Required to run on Render or Fly.io
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
