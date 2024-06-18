import smtplib

from pydantic import EmailStr
from PIL import Image
from pathlib import Path

from app.tasks.celery_app import celery
from app.tasks.email_templates import create_booking_confirmation_template
from app.config import settings


@celery.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_big = im.resize((1000, 500))
    im_resized_small = im.resize((200, 100))
    im_resized_big.save(f"app/static/images/resized_1000x500_{im_path.name}")
    im_resized_small.save(f"app/static/images/resized_200x100_{im_path.name}")


@celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):
    email_to = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(
        booking=booking,
        email_to=email_to
    )

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
