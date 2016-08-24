from __future__ import unicode_literals

from django.db import models



class AvMasterDashboard(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    short_name = models.CharField(max_length=40)
    long_name = models.CharField(max_length=150)
    description = models.CharField(max_length=400)
    dashboard_image = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    active_flag = models.CharField(max_length=1)
    last_updated_by = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'av_master_dashboard'


class AvMasterProcess(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    short_name = models.CharField(max_length=40)
    long_name = models.CharField(max_length=150)
    description = models.CharField(max_length=400)
    process_image = models.BinaryField()
    active_flag = models.CharField(max_length=1)
    last_updated_by = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'av_master_process'


class AvMasterProcessDashboards(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    process_id = models.BigIntegerField()
    dashboard_id = models.BigIntegerField()
    active_flag = models.CharField(max_length=1)
    last_updated_by = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'av_master_process_dashboards'
