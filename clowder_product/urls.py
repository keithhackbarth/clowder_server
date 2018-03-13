from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('clowder_account.urls')),
    path('', include('clowder_server.urls')),
    path('about/', TemplateView.as_view(template_name='about.html')),
    path('', TemplateView.as_view(template_name='home.html')),
    path('admin/', admin.site.urls),
]
