from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from buganim import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'server_monitor'

urlpatterns = [
    url(r'^status', views.StatusView, name='status'),
    url(r'^alerts', views.AlertsView, name='alerts'),
    url(r'^cpu', views.CPUView, name='cpu'),
    url(r'^mem', views.MEMView, name='mem'),
    url(r'^strg', views.STRGView, name='strg'),
    url(r'^net', views.NETView, name='net'),
    url(r'^graph/(?P<ip>(?:(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?)\.){3}(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?))',
        views.GraphView, name='graph'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
