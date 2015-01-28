from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'', include('clowder_server.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^admin/', include(admin.site.urls)),
)
