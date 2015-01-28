from django.conf.urls import patterns, include, url

from clowder_server.views import APIView

urlpatterns = patterns('',
    url(r'^api', APIView.as_view()),
)
