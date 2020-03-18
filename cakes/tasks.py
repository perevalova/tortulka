from django.core.mail import EmailMessage
from tortulka.celery import app
from tortulka.settings import CONTACT_EMAIL


@app.task
def send_news_email(subject, message, to_email):
    msg = EmailMessage(subject, message, CONTACT_EMAIL, [to_email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()