import datetime
import pytz

from django.core.management.base import BaseCommand, CommandError

from clowder_account.models import Company
from clowder_server.emailer import send_alert
from clowder_server.models import Alert, Ping

# Prevent overflow of database
MAXIMUM_RECORDS_PER_ACCOUNT = 10000

class Command(BaseCommand):
    help = 'Checks and sends alerts'

    def handle(self, *args, **options):

        # delete old pings
        print("Deleting old pings")
        for company in Company.objects.all():
            pings_by_name = Ping.objects.filter(company=company).distinct('name')

            if not pings_by_name:
                continue

            max_per_ping = MAXIMUM_RECORDS_PER_ACCOUNT / len(pings_by_name)

            for name in pings_by_name:
                pings = Ping.objects.filter(company=company, name=name).order_by('-create')[:max_per_ping]
                pings = list(pings.values_list("id", flat=True))
                Ping.objects.filter(company=company, name=name).exclude(pk__in=pings).delete()

        # send alerts
        print("Sending alerts")
        alerts = Alert.objects.filter(notify_at__lte=datetime.datetime.now(pytz.utc))
        for alert in alerts:
            send_alert(alert.company, alert.name)
            Ping.objects.filter(company=alert.company, name=alert.name).update(status_passing=False)
            alert.notify_at = None
            alert.save()

        # delete expired alerts
        print("Sending alerts")
        alerts = Alert.objects.filter(expire_at__lte=datetime.datetime.now(pytz.utc))
        for alert in alerts:
            Ping.objects.filter(company=alert.company, name=alert.name).delete()
            alert.delete()

# DELETE FROM clowder_server_alert
# USING (
#     SELECT id, rank() OVER (PARTITION BY clowder_server_alert.name, clowder_server_alert.company_id ORDER BY clowder_server_alert.create DESC) as rank
#     FROM clowder_server_alert
# ) AS rank
# WHERE clowder_server_alert.id = rank.id AND rank.rank > 1
