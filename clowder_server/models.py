from django.db import connection
from django.db import models

class Base(models.Model):
    name = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey('clowder_account.ClowderUser')
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

    @classmethod
    def num_passing(cls, user):
        cursor = connection.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM (
          SELECT DISTINCT ON (name)
          name, MAX(clowder_server_ping.create),
          clowder_server_ping.status_passing FROM
          clowder_server_ping WHERE user_id=73
          GROUP BY name, clowder_server_ping.status_passing
        ) AS q1 WHERE q1.status_passing=true;
        ''')
        result = cursor.fetchone()
        return result[0] if result else 0

    @classmethod
    def num_failing(cls, user):
        cursor = connection.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM (
          SELECT DISTINCT ON (name)
          name, MAX(clowder_server_ping.create),
          clowder_server_ping.status_passing FROM
          clowder_server_ping WHERE user_id=73
          GROUP BY name, clowder_server_ping.status_passing
        ) AS q1 WHERE q1.status_passing=false;
        ''')
        result = cursor.fetchone()
        return result[0] if result else 0
