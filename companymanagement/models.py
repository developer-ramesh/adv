from __future__ import unicode_literals

from django.db import models



class AvMasterCompany(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    short_name = models.CharField(max_length=40)
    full_name = models.CharField(max_length=150)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.BigIntegerField()
    primary_contact_name = models.CharField(max_length=150)
    primary_contact_email = models.CharField(max_length=150)
    primary_contact_phone = models.CharField(max_length=20)
    secondary_contact_name = models.CharField(max_length=150)
    secondary_contact_email = models.CharField(max_length=150)
    secondary_contact_phone = models.CharField(max_length=20)
    landing_page_text = models.CharField(max_length=400)
    single_sign_on_flag = models.CharField(max_length=1)
    logo = models.CharField(max_length=100)
    active_flag = models.CharField(max_length=1)
    last_updated_by = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'av_master_company'


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
    process_image = models.CharField(max_length=100)
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


class AvMasterCompanyProcess(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    company_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    no_of_licenses = models.BigIntegerField()
    active_flag = models.CharField(max_length=1)
    last_updated_by = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'av_master_company_process'


class AvMasterCompanyProcessDashboards(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    company_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    dashboard_id = models.BigIntegerField()
    active_flag = models.CharField(max_length=1)
    last_updated_by = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'av_master_company_process_dashboards'
