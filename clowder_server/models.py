from django.db import connection
from django.db import models

class Base(models.Model):
    name = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    company = models.ForeignKey('clowder_account.Company', null=True, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Alert(Base):
    """
    An alert is an alarm.
    Alerts with a notify_at value are consider future alerts.
    Alerts without a notify_at are considered failing.
    """

    notify_at = models.DateTimeField(null=True, blank=True)
    expire_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (
            ('company', 'name'),
        )

class Ping(Base):
    """
    A ping is created every time a service contacts Clowder
    A ping has a value attached that is used for graphing.
    The value can be boolean or integer or float.
    A ping also has a status.
    If a status is not explicitly passed, then a -1 is assumed to be failing
    """

    value = models.FloatField()
    public = models.BooleanField(default=False)
    status_passing = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['company', 'name', '-create']),
        ]

        index_together = (
            ('company', 'name'),
        )
