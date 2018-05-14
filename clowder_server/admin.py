from django.contrib import admin
from clowder_server.models import Alert, Ping

class PingAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'status_passing')
    list_filter = ('company',)

admin.site.register(Alert)
admin.site.register(Ping, PingAdmin)
