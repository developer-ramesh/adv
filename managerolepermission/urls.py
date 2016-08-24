from django.conf.urls import patterns, include, url
from . import views


urlpatterns = [
    url(r'^get-roles/$', views.roleIndex, name='roleIndex'),
    url(r'^role-status/$', views.roleStatus, name='roleStatus'),
    url(r'^edit-role/$', views.role_edit, name='role_edit'),
]
