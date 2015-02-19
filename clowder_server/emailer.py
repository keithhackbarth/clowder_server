from django.core.mail import send_mail

ADMIN_EMAIL = 'admin@clowder.io'

def send_alert(user, name):
    subject = 'FAILURE: %s' % (name)
    body = subject
    send_mail(subject, body, ADMIN_EMAIL, [user.email], fail_silently=False)