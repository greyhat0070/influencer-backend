import asyncio
from database.supabase_client import get_latest_summary, supabase
from utils.notifications.email_sender import send_summary_email

async def send_48hr_email_digests():
    print("📨 Running 48-hour digest scheduler...")
    subs = supabase.table("subscriptions").select("*").execute().data

    for sub in subs:
        email = sub["email"]
        handle = sub["handle"]
        platform = sub["platform"]

        summary_data = await get_latest_summary(platform, handle)
        if summary_data:
            summary = summary_data["summary"]
            subject = f"📢 48-Hour Update from @{handle} on {platform.capitalize()}"
            send_summary_email(to_email=email, subject=subject, summary=summary)
            print(f"✅ Sent to {email} for @{handle} [{platform}]")
        else:
            print(f"⚠️ No summary found for @{handle} [{platform}]")

if __name__ == "__main__":
    asyncio.run(send_48hr_email_digests())
