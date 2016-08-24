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
import time
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
def dashboardIndex(request):
    json_data=None
    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)
    process=AvMasterProcess.objects.values('id','short_name').filter(active_flag='Y').order_by('id')

    if request.method == "POST":
        if request.POST['dashboard_name']!='' and request.POST['long_name']!='' and request.POST['help_text']!='' and request.POST['dashboard_version']!='' and 'assign_process' in request.POST and  request.POST['assign_process']!=['']:
            if 'dashboard_active' in request.POST:
                role_act = 'Y'
            else:
                role_act = 'N'

            assign_process=dict(request.POST)

            if 'file' in request.FILES and request.FILES['file']!=[]:
                file_name = str(int(round(time.time() * 1000)))+'-'+str(request.FILES['file'])
                path = default_storage.save('static/uploaded/'+file_name, ContentFile(request.FILES['file'].read()))
            else:
                file_name=request.POST['edit_pic_name']

            if request.POST['dashboard_id']=='':
                chk=AvMasterDashboard.objects.filter(short_name=request.POST['dashboard_name'].strip())
                if  len(chk)==0:
                    rp=AvMasterDashboard(short_name=request.POST['dashboard_name'].strip(), long_name=request.POST['long_name'], version=request.POST['dashboard_version'],description=request.POST['help_text'],dashboard_image=file_name,active_flag=role_act,last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    rp.save()
                    add_process_in_dashboard(assign_process['assign_process'],rp.id,request.user.user_id)
                    json_data = json.dumps( { 'dashboard': get_dashboard() , 'status': 'success'} )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )
            else:
                chk=AvMasterDashboard.objects.filter(short_name=request.POST['dashboard_name'].strip()).exclude(id=request.POST['dashboard_id'])
                if  len(chk)==0:
                    AvMasterDashboard.objects.filter(id=request.POST['dashboard_id']).update(short_name=request.POST['dashboard_name'].strip(), long_name=request.POST['long_name'], version=request.POST['dashboard_version'],description=request.POST['help_text'],dashboard_image=file_name,active_flag=role_act,last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    add_process_in_dashboard(assign_process['assign_process'],request.POST['dashboard_id'],request.user.user_id)
                    json_data = json.dumps( { 'dashboard': get_dashboard() , 'status': 'success'} )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )

    else:
        json_data = json.dumps( { 'dashboard': get_dashboard(), 'process':list(process),'rolePermission':rolePermission } )

    return HttpResponse( json_data , content_type='application/json')



def get_dashboard():
    dashboard=AvMasterDashboard.objects.order_by('id')
    dashboard_json = serializers.serialize('json', dashboard )
    data_dashboard_json = json.loads( dashboard_json )
    return data_dashboard_json


@csrf_exempt
def dashboardStatus(request):
    dashboard_id=list(request.POST)
    dashboard_id=int(''.join(map(str,dashboard_id)))
    stat=AvMasterDashboard.objects.values('active_flag').filter(id=dashboard_id)
    if stat[0]['active_flag']=='Y':
        status='N'
        msg='No'
    else:
        status='Y'
        msg='Yes'

    AvMasterDashboard.objects.filter(id=dashboard_id).update(active_flag=status,last_updated_by=request.user.user_id,last_updated_date=datetime.now())

    json_data = json.dumps( {'status': 'success' , 'msg':msg, 'update_by':request.user.user_id } )
    return HttpResponse( json_data , content_type='application/json')



def add_process_in_dashboard(permisn,dashboard_id,uID):
    AvMasterProcessDashboards.objects.filter(dashboard_id=dashboard_id).delete()
    dat=''.join(map(str, permisn))
    dat.split(',')
    process=list(dat)
    for p in process:
        if p!=',':
            dat=AvMasterProcess.objects.values('id','short_name').filter(id=p)
            s=AvMasterProcessDashboards(dashboard_id=dashboard_id,process_id=dat[0]['id'],active_flag='Y',last_updated_date=datetime.now(),last_updated_by=uID)
            s.save()


@csrf_exempt
def dashboard_edit(request):
    dashboard_id=list(request.POST)
    dashboard_id=int(''.join(map(str,dashboard_id)))

    dash=AvMasterDashboard.objects.filter(id=dashboard_id)
    dash_json = serializers.serialize('json', dash )
    Data_dash_json = json.loads( dash_json )

    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)

    process=AvMasterProcess.objects.values('id','short_name').filter(active_flag='Y').order_by('id')
    user_process=AvMasterProcessDashboards.objects.values('dashboard_id','process_id').filter(dashboard_id=dashboard_id)

    user_added_process=[]
    userP=[]
    for user_perm in user_process:
        proc=AvMasterProcess.objects.values('short_name').filter(id=user_perm['process_id'])
        userP.append(user_perm['process_id'])
        user_added_process.append([user_perm['process_id'],proc[0]['short_name']])

    processP = []
    for master_perm in process:
        if master_perm['id'] not in userP:
            processP.append([master_perm['id'],master_perm['short_name']])

    json_data = json.dumps( {'status': 'success' , 'dashboard':Data_dash_json, 'user_added_process': list(user_added_process) , 'processP':processP , 'rolePermission':rolePermission} )
    return HttpResponse( json_data , content_type='application/json' )
