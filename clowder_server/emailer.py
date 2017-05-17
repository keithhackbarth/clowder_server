import os
import requests
from django.core.mail import send_mail
from clowder_account.models import ClowderUser


ADMIN_EMAIL = 'admin@clowder.io'

def send_alert(company, name):
    slack_sent = False
    for user in ClowderUser.objects.filter(company=company, allow_email_notifications=True):
        subject = 'FAILURE: %s' % (name)
        body = subject
        if user.company_id == 86 and not slack_sent:
            slack_token = os.getenv('PARKME_SLACK_TOKEN')
            url = 'https://hooks.slack.com/services/%s' % (slack_token)
            payload = {"username": "clowder", "text": body, "icon_emoji": ":clowder:"}
            requests.post(url, json=payload)
            slack_sent = True
        send_mail(subject, body, ADMIN_EMAIL, [user.email], fail_silently=True)
