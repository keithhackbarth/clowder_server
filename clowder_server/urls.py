from django.conf.urls import patterns, include, url

from clowder_server.views import APIView, DashboardView

urlpatterns = patterns('',
    url(r'^api', APIView.as_view()),
    url(r'^dashboard', DashboardView.as_view()),
)
