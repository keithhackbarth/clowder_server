from braces.views import CsrfExemptMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, View

from clowder_server.models import Ping

class APIView(CsrfExemptMixin, View):
    def post(self, request):

        name = request.POST.get('name')
        value = request.POST.get('value')

        Ping.objects.create(
            name=name,
            value=value,
        )
        return HttpResponse('ok')

class DashboardView(TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **context):
        context['pings'] = Ping.objects.all()
        return context
