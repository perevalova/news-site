from django.core.mail import send_mail
from news_project.celery import app


@app.task
def send_confirm_email(mail_subject, message, to_email):
    send_mail(mail_subject, message, 'test@newssite.com', [to_email])
