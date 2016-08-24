from django.conf.urls import patterns, include, url
from . import views


urlpatterns = [
    url(r'^upload-employee-data/$', views.uploadEmployeeData, name='uploadEmployeeData'),
    url(r'^del-file/$', views.delfile, name='delfile'),
    url(r'^roll-back3/$', views.data_rollback3, name='data_rollback3'),
    url(r'^roll-back2/$', views.data_rollback2, name='data_rollback2'),
    url(r'^roll-back/$', views.data_rollback, name='data_rollback'),
    url(r'^audit-log/$', views.auditlog, name='auditlog'),
    url(r'^get-event-subcategory/$', views.get_eventsubcategory, name='get_eventsubcategory'),
    url(r'^upload-employee-data-step2/$', views.upload_employeedata_step2, name='upload_employeedata_step2'),
    url(r'^upload-employee-data-step3/$', views.upload_employeedata_step3, name='upload_employeedata_step3'),
    url(r'^upload-employee-data-step5/$', views.upload_employeedata_step5, name='upload_employeedata_step5'),
    url(r'^upload-employee-data-step6/$', views.upload_employeedata_step6, name='upload_employeedata_step6'),
    url(r'^get-data-log/$', views.get_data_log, name='get_data_log'),
]
