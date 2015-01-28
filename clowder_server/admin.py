from django.contrib import admin
from clowder_server.models import Alert, Ping

admin.site.register(Alert)
admin.site.register(Ping)
