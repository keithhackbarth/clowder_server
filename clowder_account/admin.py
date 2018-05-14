from django.contrib import admin
from clowder_account.models import ClowderUser, Company
from clowder_server.models import Ping

class ClowderUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'public_key', 'get_full_name', 'language', 'last_login', 'number_of_pings')
    raw_id_fields = ('company',)
    list_select_related = ('company',)
    list_per_page = 50

    def public_key(self, obj):
        return obj.company.public_key
    public_key.allow_tags = True

    def number_of_pings(self, obj):
        return '%s' % (Ping.objects.filter(company=obj.company).count())
    number_of_pings.allow_tags = True


admin.site.register(ClowderUser, ClowderUserAdmin)
admin.site.register(Company)
