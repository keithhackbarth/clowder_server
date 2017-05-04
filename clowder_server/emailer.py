from django.core.mail import send_mail
from clowder_account.models import ClowderUser

ADMIN_EMAIL = 'admin@clowder.io'

def send_alert(company, name):
    for user in ClowderUser.objects.filter(company=company, allow_email_notifications=True):
        subject = 'FAILURE: %s' % (name)
        body = subject
        send_mail(subject, body, ADMIN_EMAIL, [user.email], fail_silently=True)
