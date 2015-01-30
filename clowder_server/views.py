from braces.views import CsrfExemptMixin

from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView, View

from clowder_server.models import Ping

class APIView(CsrfExemptMixin, View):
    def post(self, request):

        name = request.POST.get('name')
        value = request.POST.get('value')
        status = int(request.POST.get('status', 1))

        if status == -1:
            send_mail('Subject here', 'Here is the message.', 'admin@clowder.io',
            ['keith@parkme.com'], fail_silently=False)

        Ping.objects.create(
            name=name,
            value=value,
        )
        return HttpResponse('ok')

class DashboardView(TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **context):
        context['pings'] = Ping.objects.all().order_by(name)
        return context
