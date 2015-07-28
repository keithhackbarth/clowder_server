from django.contrib import admin
from clowder_account.models import ClowderUser, ClowderUserAdmin
from clowder_server.models import Alert, Ping

admin.site.register(Alert)
admin.site.register(ClowderUser, ClowderUserAdmin)

#@admin.register(Ping)
#class PingAdmin(admin.ModelAdmin):
#    list_filter = ('company',)
