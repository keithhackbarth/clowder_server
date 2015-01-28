from django.http import HttpResponse
from django.views.generic import View

from clowder_server.models import Ping

class APIView(View):
    def get(self, request):

        Ping.objects.create(
            name='Test'
        )
        return HttpResponse('ok')
