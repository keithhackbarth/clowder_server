import datetime

from django.core.management.base import BaseCommand, CommandError

from clowder_server.emailer import send_alert
from clowder_server.models import Alert

class Command(BaseCommand):
    help = 'Checks and sends alerts'

    def handle(self, *args, **options):
        alerts = Alert.objects.filter(notify_at__lte=datetime.datetime.now)
        for alert in alerts:
            send_alert(request.user, alert.name)
            alert.notify_at = None
            alert.save()
