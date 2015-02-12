import datetime

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from clowder_server.models import Alert

class Command(BaseCommand):
    help = 'Checks and sends alerts'

    def handle(self, *args, **options):
        alerts = Alert.objects.filter(expire_at__lte=datetime.datetime.now)
        for alert in alerts:
            send_mail('Subject here', 'Here is the message.', 'admin@clowder.io',
                    ['keith@parkme.com'], fail_silently=False)
            alert.delete()
