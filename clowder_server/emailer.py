import os
import requests
from django.core.mail import send_mail
from clowder_account.models import ClowderUser


ADMIN_EMAIL = 'admin@clowder.io'

def send_alert(company, name):
    for user in ClowderUser.objects.filter(company=company):
        subject = 'FAILURE: %s' % (name)
        body = subject
        slack_token = os.getenv('PARKME_SLACK_TOKEN')
        url = 'https://hooks.slack.com/services/%s' % (slack_token)
        payload = {"username": "devopsbot", "text": body, "icon_emoji": ":robot_face:"}
        requests.post(url, json=payload)
        send_mail(subject, body, ADMIN_EMAIL, [user.email], fail_silently=True)
