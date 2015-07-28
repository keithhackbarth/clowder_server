import datetime

from django.core.management.base import BaseCommand, CommandError

from clowder_account.models import Company
from clowder_server.emailer import send_alert
from clowder_server.models import Alert, Ping

class Command(BaseCommand):
    help = 'Checks and sends alerts'

    def handle(self, *args, **options):

        # delete old pings
        for company in Company.objects.all():
            pings = Ping.objects.filter(company=company).order_by('-create')[:500]
            pings = list(pings.values_list("id", flat=True))
            Ping.objects.filter(company=company).exclude(pk__in=pings).delete()

        # send alerts
        alerts = Alert.objects.filter(notify_at__lte=datetime.datetime.now)
        for alert in alerts:
            send_alert(alert.user, alert.name)
            alert.notify_at = None
            alert.save()
