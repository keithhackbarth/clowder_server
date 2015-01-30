from django.db import models

class Alert(models.Model):
    name = models.CharField(max_length=200)
    expire_at = models.DateTimeField()

class Ping(models.Model):
    name = models.CharField(max_length=200)
    value = models.FloatField()
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
