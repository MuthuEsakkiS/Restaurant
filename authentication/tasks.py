from foodiee.celery import app
from django.core.mail import send_mail
import time


@app.task(name='send_mail')
def send_email_fun(subject, message, sender, receiver):
    time.sleep(5)
    send_mail(subject, message, sender, [receiver])
