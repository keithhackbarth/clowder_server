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
            pings_by_name = Ping.objects.filter(company=company).distinct('name')

            if not pings_by_name:
                continue

            max_per_ping = 2000 / len(pings_by_name)

            for name in pings_by_name:
                pings = Ping.objects.filter(company=company, name=name).order_by('-create')[:max_per_ping]
                pings = list(pings.values_list("id", flat=True))
                Ping.objects.filter(company=company, name=name).exclude(pk__in=pings).delete()

        # send alerts
        alerts = Alert.objects.filter(notify_at__lte=datetime.datetime.now)
        for alert in alerts:
            send_alert(alert.company, alert.name)
            alert.notify_at = None
            alert.save()



# DELETE FROM clowder_server_alert
# USING (
#     SELECT id, rank() OVER (PARTITION BY clowder_server_alert.name, clowder_server_alert.company_id ORDER BY clowder_server_alert.create DESC) as rank
#     FROM clowder_server_alert
# ) AS rank
# WHERE clowder_server_alert.id = rank.id AND rank.rank > 1
