from django.conf.urls import patterns, url

from clowder_account.views import RegisterView

urlpatterns = patterns('',

    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
       {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'}),
    url(r'^accounts/register/$', RegisterView.as_view())

)
