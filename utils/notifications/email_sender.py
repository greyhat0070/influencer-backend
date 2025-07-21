# notifications/email_sender.py

import os
import resend

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
resend.api_key = RESEND_API_KEY

def send_summary_email(to_email: str, subject: str, summary: str):
    try:
        response = resend.Emails.send({
            "from": "Influencer Agent <onboarding@resend.dev>",  # default testing domain
            "to": [to_email],
            "subject": subject,
            "text": summary,
        })
        return {"status": "sent", "data": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
