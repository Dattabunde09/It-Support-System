# tickets/utils.py
import resend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# set Resend API key
resend.api_key = settings.RESEND_API_KEY

def send_welcome_email(user, verify_link):
    """Send welcome email with verification link via Resend"""
    try:
        result = resend.Emails.send({
            "from": "onboarding@resend.dev",  # you can change to your verified Resend sender
            "to": user.email,
            "subject": "Welcome to IT Support System – Verify Your Email",
            "html": f"""
                <h3>Welcome {user.username}!</h3>
                <p>Click the link below to verify your account:</p>
                <a href="{verify_link}">Verify Email</a>
            """
        })
        logger.info(f"Verification email sent successfully to {user.email}")
        return result
    except Exception as e:
        logger.error(f"Error sending verification email to {user.email}: {str(e)}")
        raise
