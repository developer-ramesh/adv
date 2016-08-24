from django.conf.urls import patterns, include, url
from . import views


urlpatterns = [
    url(r'^get-message/$', views.messageIndex, name='messageIndex'),
    url(r'^message-status/$', views.messageStatus, name='messageStatus'),
    url(r'^edit-message/$', views.message_edit, name='message_edit'),
]
