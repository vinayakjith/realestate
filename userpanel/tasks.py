from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_otp_mail(email, otp):
    subject="Your OTP for password reset"
    message=f'Your OTP is {otp}. It is valid for 10 minutes. Please do not share this with anyone.'
    send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[email])



