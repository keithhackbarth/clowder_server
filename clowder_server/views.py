from braces.views import CsrfExemptMixin, LoginRequiredMixin
import datetime
from ipware.ip import get_real_ip
import pytz

from django.http import HttpResponse
from django.contrib.auth import decorators
from django.views.generic import TemplateView, View

from clowder_account.models import Company
from clowder_server.emailer import send_alert
from clowder_server.models import Alert, Ping

class APIView(CsrfExemptMixin, View):

    def post(self, request):

        name = request.POST.get('name')
        frequency = request.POST.get('frequency')
        value = request.POST.get('value', 1)
        api_key = request.POST.get('api_key')
        status = int(request.POST.get('status', 1))
        public = bool(request.POST.get('public'))

        company = Company.objects.get(public_key=api_key)
        ip = get_real_ip(request) or '127.0.0.1'

        if not name:
            return HttpResponse('name needed')

        # drop old alerts
        already_sent_email = Alert.objects.filter(name=name, notify_at__isnull=True).exists()
        Alert.objects.filter(name=name).delete()

        if status == -1:
            if not already_sent_email:
                send_alert(company, name)

            Alert.objects.create(
                name=name,
                company=company,
                ip_address=ip,
            )

        elif frequency:
            expiration_date = (
                datetime.datetime.now(pytz.utc) +
                datetime.timedelta(seconds=int(frequency))
            )

            Alert.objects.create(
                name=name,
                company=company,
                notify_at=expiration_date,
                ip_address=ip,
            )

        Ping.objects.create(
            name=name,
            company=company,
            value=value,
            ip_address=ip,
            status_passing=(status == 1),
            public=public,
        )
        return HttpResponse('ok')


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"

    def _pings(self, user):
        return Ping.objects.filter(company=user.company).order_by('name', 'create')

    def _total_num_pings(self, user):
        return self._pings(user).distinct('name').count()

    def get(self, request, *args, **kwargs):
        context = {
            'pings': self._pings(request.user),
        }
        total_num_pings = self._total_num_pings(request.user)
        if total_num_pings:
            context['num_passing'] = Ping.num_passing(request.user.company_id)
            context['num_failing'] = Ping.num_failing(request.user.company_id)
            context['total_num_pings'] = total_num_pings
            context['percent_passing'] = round(
                (float(context['num_passing']) / float(total_num_pings)) * 100
            )
        return self.render_to_response(context)


class PublicView(TemplateView):

    template_name = "dashboard.html"

    def _pings(self, company):
        return Ping.objects.filter(
            company=company,
            public=True
        ).order_by('name', 'create')

    def _total_num_pings(self, company):
        return self._pings(company).distinct('name').count()

    def get(self, request, secret_key):

        company = Company.objects.get(secret_key=secret_key)

        context = {
            'pings': self._pings(company),
            'public': True
        }
        total_num_pings = self._total_num_pings(company)
        if total_num_pings:
            context['num_passing'] = Ping.num_passing(company.id)
            context['num_failing'] = Ping.num_failing(company.id)
            context['total_num_pings'] = total_num_pings
            context['percent_passing'] = round(
                (float(context['num_passing']) / float(total_num_pings)) * 100
            )
        return self.render_to_response(context)


class DeleteView(CsrfExemptMixin, View):

    @decorators.login_required
    def get(self, request, *args, **kwargs):
        Ping.objects.filter(company=request.user.company).delete()
        Alert.objects.filter(company=request.user.company).delete()
        return HttpResponse('ok')

    def post(self, request, *args, **kwargs):
        api_key = request.POST.get('api_key')
        name = request.POST.get('name')

        company = Company.objects.get(public_key=api_key)

        if name:
            Ping.objects.filter(company=company, name=name).delete()
            Alert.objects.filter(company=company, name=name).delete()
            return HttpResponse('deleted')

        return HttpResponse('ok')
