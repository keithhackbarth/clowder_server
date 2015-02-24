from braces.views import CsrfExemptMixin, LoginRequiredMixin
import datetime
from ipware.ip import get_real_ip
import pytz

from django.http import HttpResponse
from django.views.generic import TemplateView, View

from clowder_account.models import ClowderUser
from clowder_server.emailer import send_alert
from clowder_server.models import Alert, Ping

class APIView(CsrfExemptMixin, View):
    def post(self, request):

        name = request.POST.get('name')
        frequency = request.POST.get('frequency')
        value = request.POST.get('value')
        api_key = request.POST.get('api_key')
        status = int(request.POST.get('status', 1))

        user = ClowderUser.objects.get(public_key=api_key)
        ip = get_real_ip(request)

        if status == -1:
            send_alert(request.user, name)

            Alert.objects.create(
                name=name,
                user=user,
                ip_address=ip,
            )

        elif frequency:
            expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=int(frequency))

            Alert.objects.filter(name=name).delete()

            Alert.objects.create(
                name=name,
                user=user,
                notify_at=expiration_date,
                ip_address=ip,
            )

        Ping.objects.create(
            name=name,
            user=user,
            value=value,
            ip_address=ip,
        )
        return HttpResponse('ok')

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"

    def _pings(self, user):
        three_days = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=3)
        return Ping.objects.filter(user=user, create__gte=three_days).order_by('name', 'create')

    def get(self, request, *args, **kwargs):
        context = {'pings': self._pings(request.user)}
        return self.render_to_response(context)
