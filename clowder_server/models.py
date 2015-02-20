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
