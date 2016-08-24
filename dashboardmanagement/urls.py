from django.conf.urls import patterns, include, url
from . import views


urlpatterns = [
    url(r'^get-dashboard/$', views.dashboardIndex, name='dashboardIndex'),
    url(r'^dashboard-status/$', views.dashboardStatus, name='dashboardStatus'),
    url(r'^edit-dashboard/$', views.dashboard_edit, name='dashboard_edit'),
]
