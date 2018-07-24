import os
import requests
from django.core.mail import send_mail
from clowder_account.models import ClowderUser


ADMIN_EMAIL = 'admin@clowder.io'

def send_alert(alert):

    subject = 'FAILURE: %s' % (alert.name)

    if alert.company_id == 86:
        slack_token = os.getenv('PARKME_SLACK_TOKEN')
        url = 'https://hooks.slack.com/services/%s' % (slack_token)
        payload = {"username": "clowder", "text": subject, "icon_emoji": ":clowder:"}
        requests.post(url, json=payload)

    if alert.send_email:
        for user in ClowderUser.objects.filter(company_id=alert.company_id):
            body = subject
            send_mail(subject, body, ADMIN_EMAIL, [user.email], fail_silently=True)
