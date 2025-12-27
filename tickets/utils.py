# ================= EMAIL UTILS =================

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_welcome_email(user, verify_link):
    subject = "Welcome to IT Support System – Verify Your Email"

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
    email.send()
