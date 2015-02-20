from django.contrib.auth import authenticate, login
from django.views.generic.base import RedirectView

from clowder_account.models import ClowderUser

class RegisterView(RedirectView):

    url = '/dashboard'

    def post(self, request, *args, **kwargs):

        email = request.POST['email']
        password = request.POST['password']

        user = ClowderUser.objects.create_user(email, password)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.language = request.POST['language']

        user = authenticate(username=email, password=password)
        login(request, user)

        return self.get(request, *args, **kwargs)
