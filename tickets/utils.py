# ================= EMAIL UTILS =================

import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)

def send_welcome_email(user, verify_link):
    """Send welcome email with verification link"""
    subject = "Welcome to IT Support System – Verify Your Email"

    try:
        html_content = render_to_string(
            "tickets/welcome_verify.html",
            {
                "user": user,
                "verify_link": verify_link,
            }
        )

        email = EmailMultiAlternatives(
            subject,
            "",
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )

        email.attach_alternative(html_content, "text/html")
        result = email.send()

        if result == 1:
            logger.info(f"Verification email sent successfully to {user.email}")
        else:
            logger.error(f"Failed to send verification email to {user.email}")

        return result

    except Exception as e:
        logger.error(f"Error sending verification email to {user.email}: {str(e)}")
        raise
