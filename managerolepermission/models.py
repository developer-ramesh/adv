from __future__ import unicode_literals

from django.db import models



class AvMasterRoles(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    role_name = models.CharField(max_length=240)
    description = models.CharField(max_length=400)
    restricted_flag = models.CharField(max_length=1)
    active_flag = models.CharField(max_length=1)
    last_updated_by = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'av_master_roles'


class AvMasterPermissions(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    permission = models.CharField(max_length=240)
    description = models.CharField(max_length=400)
    active_flag = models.CharField(max_length=1)
    last_updated_by = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'av_master_permissions'

class AvMasterRolePermissions(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    role_id = models.BigIntegerField()
    permission_id = models.BigIntegerField()
    comments = models.CharField(max_length=400)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_role_permissions'


class AvMasterUserRoles(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    company_id = models.BigIntegerField()
    user_id = models.CharField(max_length=30)
    role_id = models.BigIntegerField()
    comments = models.CharField(max_length=400)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_user_roles'
