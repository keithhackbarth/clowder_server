from django.conf.urls import patterns, include, url

from clowder_server.views import APIView, DashboardView, DeleteView, PublicView

urlpatterns = patterns('',
    url(r'^api', APIView.as_view()),
    url(r'^dashboard', DashboardView.as_view()),
    url(r'^public/(?P<secret_key>\w+)/', PublicView.as_view()),
    url(r'^delete', DeleteView.as_view()),
)
