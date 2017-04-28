from django.conf.urls import url
import django.contrib.auth.views

from clowder_account.views import AccountView, RegisterView

urlpatterns = [
    url(r'^accounts/login/$', django.contrib.auth.views.login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, {'template_name': 'logout.html'}),
    url(r'^accounts/register/$', RegisterView.as_view()),
    url(r'^accounts/$', AccountView.as_view())
]
