from django.conf.urls import patterns, include, url
from . import views


urlpatterns = [
    url(r'^get-company/$', views.companyIndex, name='companyIndex'),
    url(r'^company-status/$', views.companyStatus, name='companyStatus'),
    url(r'^edit-company/$', views.company_edit, name='company_edit'),
    url(r'^company-licenses/$', views.company_licenses, name='company_licenses'),
    url(r'^company-licenses-update/$', views.update_company_licenses, name='update_company_licenses'),
    url(r'^company-dashboard/$', views.company_dashboards, name='company_dashboards'),
    url(r'^company-dashboard-update/$', views.update_company_dashboard, name='update_company_dashboard'),
]
