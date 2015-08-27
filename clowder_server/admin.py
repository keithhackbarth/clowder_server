from django.contrib import admin
from clowder_account.models import ClowderUser, ClowderUserAdmin, Company
from clowder_server.models import Alert, Ping

admin.site.register(Alert)
admin.site.register(ClowderUser, ClowderUserAdmin)
admin.site.register(Company)

@admin.register(Ping)
class PingAdmin(admin.ModelAdmin):
    list_filter = ('company',)
