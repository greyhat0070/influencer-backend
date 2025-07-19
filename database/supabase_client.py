import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # Only needed for local development

# ✅ Correct way: get by variable name, NOT value
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_KEY in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def insert_summary(platform, handle, content, summary):
    data = {
        "platform": platform,
        "handle": handle,
        "content": content,
        "summary": summary
    }
    supabase.table("influencers").insert(data).execute()
