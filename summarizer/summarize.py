from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn

from fetchers.insta_linkedin_scraper import fetch_instagram_posts, fetch_linkedin_posts
from fetchers.youtube_fetcher import fetch_youtube_videos
from summarizer.summarize import summarize_text
from database.supabase_client import insert_summary, get_latest_summary
from utils.notifications.email_sender import send_summary_email

app = FastAPI()

# ===================== CORS ===================== #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== MODELS ===================== #
class SummaryRequest(BaseModel):
    handle: str
    platform: str  # youtube | instagram | linkedin

# ===================== ROUTES ===================== #

@app.get("/fetch/instagram")
def fetch_instagram(handle: str = Query(...)):
    try:
        return fetch_instagram_posts(handle)
    except Exception as e:
        return {"error": f"Instagram fetch failed: {str(e)}"}

@app.get("/fetch/linkedin")
def fetch_linkedin(handle: str = Query(...)):
    try:
        return fetch_linkedin_posts(handle)
    except Exception as e:
        return {"error": f"LinkedIn fetch failed: {str(e)}"}

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
        return {"error": f"YouTube fetch failed: {str(e)}"}

@app.post("/summarize/")
async def summarize_content(req: SummaryRequest):
    try:
        platform = req.platform.lower()

        if platform == "instagram":
            posts = fetch_instagram_posts(req.handle)
        elif platform == "linkedin":
            posts = fetch_linkedin_posts(req.handle)
        else:
            return {"error": "Unsupported platform"}

        if isinstance(posts, dict) and "error" in posts:
            return posts

        combined_text = "\n\n".join([p["title"] + "\n" + p["description"] for p in posts])
        summary = await summarize_text(combined_text)

        await insert_summary(
            platform=platform.capitalize(),
            handle=req.handle,
            content=combined_text,
            summary=summary
        )

        return {
            "platform": platform,
            "handle": req.handle,
            "summary": summary
        }
    except Exception as e:
        return {"error": f"Summarization failed: {str(e)}"}

@app.post("/send-email/")
async def trigger_email(to: str, handle: str, platform: str):
    try:
        data = await get_latest_summary(platform, handle)

        if not data:
            return {"error": "No summary found"}

        summary = data["summary"]
        subject = f"🔥 {platform.capitalize()} Summary for @{handle}"
        return send_summary_email(to_email=to, subject=subject, summary=summary)
    except Exception as e:
        return {"error": f"Email sending failed: {str(e)}"}


# ===================== ENTRY ===================== #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
