from django.conf.urls import patterns, include, url
from . import views


urlpatterns = [
    url(r'^get-highdoller-data/$', views.getSearchHighDoller, name='getSearchHighDoller'),
    url(r'^get-detail-records/$', views.getDetailRecords, name='getDetailRecords'),
]
