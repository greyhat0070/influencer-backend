from fastapi import FastAPI
from fetchers.youtube_fetcher import fetch_youtube_videos
from summarizer.summarize import summarize_text
from database.supabase_client import insert_summary

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Influencer Monitoring Agent is running"}
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # dynamically use Render's port
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

@app.get("/fetch/youtube")
async def fetch_youtube(handle: str):
    videos = await fetch_youtube_videos(handle)
    full_text = " ".join([v["title"] + " " + v["description"] for v in videos])
    summary = summarize_text(full_text)
    await insert_summary(platform="YouTube", handle=handle, content=full_text, summary=summary)
    return {"summary": summary}
