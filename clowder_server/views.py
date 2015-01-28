from django.http import HttpResponse
from django.views.generic import TemplateView, View

from clowder_server.models import Ping

class APIView(View):
    def get(self, request):

        Ping.objects.create(
            name='Test'
        )
        return HttpResponse('ok')

class DashboardView(TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **context):
        context['pings'] = Ping.objects.all()
        return context
