from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core import serializers
import json
from django.db.models import Sum, Count
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.template import Context
from datetime import datetime, timedelta
from django.db import connection
import pyexcel as pe
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from collections import defaultdict,OrderedDict
import utilb
import xlwt


@csrf_exempt
def roleIndex(request):
    json_data=None
    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)

    permission=''
    if 'Manage Restricted Role' in rolePermission:
        permission=AvMasterPermissions.objects.values('id','permission').filter(active_flag='Y').order_by('id')
    else:
        permission=AvMasterPermissions.objects.values('id','permission').filter(active_flag='Y').exclude(permission='Manage Restricted Role').order_by('id')

    if request.method == "POST":
        if request.POST['role_name']!='' and request.POST['role_description']!='' and 'assign_permission' in request.POST and  request.POST['assign_permission']!=['']:
            if 'role_active' in request.POST:
                role_act = 'Y'
            else:
                role_act = 'N'

            if 'role_restricted' in request.POST:
                role_restric = 'Y'
            else:
                role_restric = 'N'

            assign_permission=dict(request.POST)

            if request.POST['role_id']=='':
                chk=AvMasterRoles.objects.filter(role_name=request.POST['role_name'].strip())
                if  len(chk)==0:
                    rp=AvMasterRoles(role_name=request.POST['role_name'].strip(), description=request.POST['role_description'], restricted_flag=role_restric,active_flag=role_act,last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    rp.save()
                    add_permission_in_role(assign_permission['assign_permission'],rp.id,request.user.user_id)
                    json_data = json.dumps( { 'dataRole': get_roles() , 'status': 'success'} )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )
            else:
                chk=AvMasterRoles.objects.filter(role_name=request.POST['role_name'].strip()).exclude(id=request.POST['role_id'])
                if  len(chk)==0:
                    AvMasterRoles.objects.filter(id=request.POST['role_id']).update(role_name=request.POST['role_name'].strip(), description=request.POST['role_description'], restricted_flag=role_restric,active_flag=role_act,last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    add_permission_in_role(assign_permission['assign_permission'],request.POST['role_id'],request.user.user_id)
                    json_data = json.dumps( { 'dataRole': get_roles() , 'status': 'success'} )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )

    else:
        json_data = json.dumps( { 'dataRole': get_roles() ,'permission': list(permission), 'rolePermission':rolePermission } )

    return HttpResponse( json_data , content_type='application/json')


@csrf_exempt
def roleStatus(request):
    role_id=list(request.POST)
    role_id=int(''.join(map(str,role_id)))
    stat=AvMasterRoles.objects.values('active_flag').filter(id=role_id)
    if stat[0]['active_flag']=='Y':
        status='N'
        msg='No'
    else:
        status='Y'
        msg='Yes'

    AvMasterRoles.objects.filter(id=role_id).update(active_flag=status,last_updated_by=request.user.user_id,last_updated_date=datetime.now())
    AvMasterUserRoles.objects.filter(role_id=role_id).update(active_flag=status,last_updated_by=request.user.user_id,last_updated_date=datetime.now())

    json_data = json.dumps( {'status': 'success' , 'msg':msg , 'update_by':request.user.user_id } )
    return HttpResponse( json_data , content_type='application/json')


def add_permission_in_role(permisn,role_id,uID):
    AvMasterRolePermissions.objects.filter(role_id=role_id).delete()
    for perm in permisn:
        dat=AvMasterPermissions.objects.values('id','permission').filter(id=perm)
        s=AvMasterRolePermissions(role_id=role_id,permission_id=dat[0]['id'],comments=dat[0]['permission'],active_flag='Y',last_updated_date=datetime.now(),last_updated_by=uID)
        s.save()


def get_roles():
    role=AvMasterRoles.objects.order_by('id')
    role_json = serializers.serialize('json', role )
    Data_role_json = json.loads( role_json )
    return Data_role_json


@csrf_exempt
def role_edit(request):
    role_id=list(request.POST)
    role_id=int(''.join(map(str,role_id)))
    role=AvMasterRoles.objects.filter(id=role_id)
    role_json = serializers.serialize('json', role )
    Data_role_json = json.loads( role_json )

    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)
    permissions=''
    if 'Manage Restricted Role' in rolePermission:
        permissions=AvMasterPermissions.objects.values('id','permission').filter(active_flag='Y').order_by('id')
    else:
        permissions=AvMasterPermissions.objects.values('id','permission').filter(active_flag='Y').exclude(permission='Manage Restricted Role').order_by('id')

    user_permission=AvMasterRolePermissions.objects.values('permission_id','comments').filter(role_id=role_id)

    userP=[]
    for user_perm in user_permission:
        userP.append(user_perm['permission_id'])

    permissionsP = []
    for master_perm in permissions:
        if master_perm['id'] not in userP:
            permissionsP.append([master_perm['id'],master_perm['permission']])

    json_data = json.dumps( {'status': 'success' , 'role':Data_role_json, 'user_permission': list(user_permission) , 'permissions':permissionsP , 'rolePermission':rolePermission} )
    return HttpResponse( json_data , content_type='application/json' )
