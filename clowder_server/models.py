from django.db import connection
from django.db import models

class Base(models.Model):
    name = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    company = models.ForeignKey('clowder_account.Company', null=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Alert(Base):
    notify_at = models.DateTimeField(null=True, blank=True)


class Ping(Base):
    value = models.FloatField()
    status_passing = models.BooleanField(default=True)

    def get_closest_alert(self):
        return Alert.objects.filter(
            name=self.name,
            ip_address=self.ip_address,
            company=self.company,
        ).order_by('notify_at').first()

    @classmethod
    def num_passing(cls, company_id):
        cursor = connection.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM (
          SELECT
            name,
            rank() OVER (PARTITION BY name ORDER BY clowder_server_ping.create DESC) as rank,
            status_passing
          FROM clowder_server_ping
          WHERE company_id = %s
        ) AS q1
          WHERE status_passing = true
          AND rank = 1;
        ''', [company_id])
        result = cursor.fetchone()
        return result[0] if result else 0

    @classmethod
    def num_failing(cls, company_id):
        cursor = connection.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM (
          SELECT
            name,
            rank() OVER (PARTITION BY name ORDER BY clowder_server_ping.create DESC) as rank,
            status_passing
          FROM clowder_server_ping
          WHERE company_id = %s
        ) AS q1
          WHERE status_passing = false
          AND rank = 1;
        ''', [company_id])
        result = cursor.fetchone()
        return result[0] if result else 0
