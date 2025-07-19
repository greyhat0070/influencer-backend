import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("https://heamfsqjsxzfkvjxhakz.supabase.co")
key = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhlYW1mc3Fqc3h6Zmt2anhoYWt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI5MDUxMDgsImV4cCI6MjA2ODQ4MTEwOH0.drhdPR5WlYVV1Sye6_NxLjPutbToQgIOyn4gWgXc0bA")

supabase = create_client(url, key)

async def insert_summary(platform, handle, content, summary):
    data = {
        "platform": platform,
        "handle": handle,
        "content": content,
        "summary": summary
    }
    supabase.table("influencers").insert(data).execute()
