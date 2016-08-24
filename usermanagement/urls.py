from django.conf.urls import patterns, include, url
from . import views


urlpatterns = [
    url(r'^get-user/$', views.userIndex, name='userIndex'),
    url(r'^user-status/$', views.userStatus, name='userStatus'),
    url(r'^get-assign_data/$', views.getAssignData, name='getAssignData'),
    url(r'^add-user-assign_data/$', views.add_user_assign_data, name='add_user_assign_data'),
]
