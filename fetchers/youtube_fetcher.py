import httpx
import os
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

async def fetch_youtube_videos(channel_id: str):
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&part=snippet&type=video&maxResults=5"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        videos = []
        for item in res.json().get("items", []):
            snippet = item["snippet"]
            videos.append({
                "title": snippet["title"],
                "description": snippet["description"]
            })
        return videos
