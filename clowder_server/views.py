from braces.views import CsrfExemptMixin, LoginRequiredMixin
import datetime
from ipware.ip import get_real_ip
import pytz

from django.http import HttpResponse
from django.contrib.auth import decorators
from django.views.generic import TemplateView, View

from clowder_account.models import ClowderUser
from clowder_server.emailer import send_alert
from clowder_server.models import Alert, Ping

class APIView(CsrfExemptMixin, View):

    def post(self, request):

        name = request.POST.get('name')
        frequency = request.POST.get('frequency')
        value = request.POST.get('value', 1)
        api_key = request.POST.get('api_key')
        status = int(request.POST.get('status', 1))

        user = ClowderUser.objects.get(public_key=api_key)
        ip = get_real_ip(request) or '127.0.0.1'

        if not name:
            return HttpResponse('name needed')

        if status == -1:
            send_alert(user, name)

            Alert.objects.create(
                name=name,
                user=user,
                ip_address=ip,
            )

        elif frequency:
            expiration_date = (
                datetime.datetime.now() +
                datetime.timedelta(seconds=int(frequency))
            )

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
            status_passing=(status == 1)
        )
        return HttpResponse('ok')

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"

    def _pings(self, user):
        three_days = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=3)
        return Ping.objects.filter(
            user=user, create__gte=three_days
        ).order_by('name', 'create')

    def _num_passing_pings(self, user):
        three_days = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=3)
        return Ping.objects.filter(
            user=user, status_passing=True, create__gte=three_days
        ).distinct('name').order_by('create').count()

    def _num_failing_pings(self, user):
        three_days = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=3)
        return Ping.objects.filter(
            user=user, status_passing=False, create__gte=three_days
        ).distinct('name').count()

    def _total_num_pings(self, user):
        return self._pings(user).distinct('name').count()

    def get(self, request, *args, **kwargs):
        context = {
            'pings': self._pings(request.user),
        }
        total_num_pings = self._total_num_pings(request.user)
        if total_num_pings:
            context['num_passing'] = self._num_passing_pings(request.user)
            context['num_failing'] = self._num_failing_pings(request.user)
            context['total_num_pings'] = total_num_pings
            context['percent_passing'] = round(
                (float(context['num_passing']) / float(total_num_pings)) * 100
            )
        return self.render_to_response(context)


class DeleteView(CsrfExemptMixin, View):

    @decorators.login_required
    def get(self, request, *args, **kwargs):
        Ping.objects.filter(user=request.user).delete()
        Alert.objects.filter(user=request.user).delete()
        return HttpResponse('ok')

    def post(self, request, *args, **kwargs):
        api_key = request.POST.get('api_key')
        name = request.POST.get('name')

        user = ClowderUser.objects.get(public_key=api_key)

        if name:
            Ping.objects.filter(user=user, name=name).delete()
            Alert.objects.filter(user=user, name=name).delete()
            return HttpResponse('deleted')

        return HttpResponse('ok')
