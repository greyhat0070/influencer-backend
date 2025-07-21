import httpx
import os
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Use correct .env key name

# Get actual channelId from a handle or username
async def resolve_channel_id(handle: str) -> str:
    handle = handle.lstrip("@")

    # First try handle lookup (new YouTube API beta feature)
    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={handle}&key={YOUTUBE_API_KEY}"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()
        items = data.get("items", [])
        if items:
            return items[0]["id"]

    # Fallback to forUsername lookup
    fallback_url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={handle}&key={YOUTUBE_API_KEY}"
    async with httpx.AsyncClient() as client:
        res = await client.get(fallback_url)
        data = res.json()
        items = data.get("items", [])
        if items:
            return items[0]["id"]

    print(f"❌ Could not resolve channel ID for handle: {handle}")
    return None

# Fetch recent videos
async def fetch_youtube_videos(handle: str):
    channel_id = await resolve_channel_id(handle)
    if not channel_id:
        return []

    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&part=snippet&type=video&maxResults=5"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()
        videos = []
        for item in data.get("items", []):
            snippet = item["snippet"]
            videos.append({
                "title": snippet.get("title", ""),
                "description": snippet.get("description", "")
            })
        return videos
