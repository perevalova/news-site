from django.core.mail import send_mail
from news_project.celery import app
from news_project.settings import DEFAULT_FROM_EMAIL


@app.task
def send_email_user(mail_subject, message, to_email):
    send_mail(mail_subject, message, DEFAULT_FROM_EMAIL, [to_email])
