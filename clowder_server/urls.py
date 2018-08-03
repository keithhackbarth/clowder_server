from django.conf.urls import include, url
from django.conf import settings

from clowder_server.views import APIView, DeleteView, PrivateView, PublicView

urlpatterns = [
    url(r'^api', APIView.as_view()),
    url(r'^dashboard', PrivateView.as_view()),
    url(r'^public/(?P<secret_key>\w+)/', PublicView.as_view()),
    url(r'^delete', DeleteView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
