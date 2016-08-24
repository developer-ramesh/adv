"""audvantage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import patterns, include, url
from administrator.views import *

urlpatterns = [
    url('', include('usermanagement.urls')),
    url('', include('messagemanagement.urls')),
    url('', include('companymanagement.urls')),
    url('', include('dashboardmanagement.urls')),
    url('', include('processmanagement.urls')),
    url('', include('managerolepermission.urls')),
    url('', include('dashboard.urls')),
    url('', include('datamanagement.urls')),
    url(r'^get-summary-data/$', getSearchSummary),
    url(r'^$', admin_home),
    url(r'^login/$', login),
    url(r'^forgot-username/$', forgotUserName),
    url(r'^forgot-password/$', forgotPassword),
    url(r'^reset-password/(.*)/$', resetPassword),
    url(r'^logout/$', logout_page),
]
