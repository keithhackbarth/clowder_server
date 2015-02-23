from django.contrib import admin
from clowder_account.models import ClowderUser
from clowder_server.models import Alert, Ping

admin.site.register(Alert)
admin.site.register(ClowderUser)
admin.site.register(Ping)
