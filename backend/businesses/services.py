import random
import string
from django.core.mail import send_mail
from django.conf import settings
from core.settings.base import EMAIL_HOST_USER
from django.template.loader import render_to_string
from PIL import Image
import numpy as np

# from django.shortcuts import render


def generate_otp(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_email(email, otp):
    subject = "Your OTP for Register"
    # Sử dụng hàm render_to_string để render template HTML
    html_message = render_to_string("businesses/emails/otp_email_template.html", {"otp": otp})
    message = f"Your OTP is: {otp}"
    from_email = EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    
