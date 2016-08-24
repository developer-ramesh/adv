from django.conf.urls import patterns, include, url
from . import views


urlpatterns = [
    url(r'^get-process/$', views.processIndex, name='processIndex'),
    url(r'^process-status/$', views.processStatus, name='processStatus'),
    url(r'^edit-process/$', views.process_edit, name='process_edit'),
]
