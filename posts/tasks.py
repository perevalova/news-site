import datetime

from django.core.mail import send_mail
from news_project.celery import app
from posts.models import Post


@app.task
def send_comment_email(mail_subject, message, to_email):
    send_mail(mail_subject, message, 'test@newssite.com', [to_email])
