import instaloader
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
load_dotenv()


def fetch_instagram_posts(handle: str, max_posts: int = 10):
    L = instaloader.Instaloader()
    posts_data = []
    try:
        profile = instaloader.Profile.from_username(L.context, handle)
        for post in profile.get_posts():
            if len(posts_data) >= max_posts:
                break
            posts_data.append({
                "title": post.caption.split("\n")[0] if post.caption else "No Title",
                "description": post.caption or "No Description"
            })
    except Exception as e:
        return {"error": str(e)}
    return posts_data

def fetch_linkedin_posts(handle: str):
    try:
        search = GoogleSearch({
            "q": f"site:linkedin.com/in {handle}",
            "api_key": os.getenv("SERPAPI_KEY")
        })
        results = search.get_dict()
        linkedin_snippets = []

        for result in results.get("organic_results", []):
            if "linkedin.com/in/" in result.get("link", ""):
                linkedin_snippets.append({
                    "title": result.get("title", "No Title"),
                    "description": result.get("snippet", "No Description")
                })

        return linkedin_snippets
    except Exception as e:
        return {"error": str(e)}
