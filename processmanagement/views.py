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
def processIndex(request):
    json_data=None
    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)
    dashboard=AvMasterDashboard.objects.values('id','short_name').filter(active_flag='Y').order_by('id')

    if request.method == "POST":
        if request.POST['process_name']!='' and request.POST['long_name']!='' and request.POST['help_text']!='' and 'assign_dashboard' in request.POST and  request.POST['assign_dashboard']!=['']:
            role_act=request.POST['process_active']
            assign_dashboard=dict(request.POST)

            if 'file' in request.FILES and request.FILES['file']!=[]:
                file_name = str(int(round(time.time() * 1000)))+'-'+str(request.FILES['file'])
                path = default_storage.save('static/uploaded/'+file_name, ContentFile(request.FILES['file'].read()))
            else:
                file_name=request.POST['edit_pic_name']

            if request.POST['process_id']=='':
                chk=AvMasterProcess.objects.filter(short_name=request.POST['process_name'].strip())
                if  len(chk)==0:
                    rp=AvMasterProcess(short_name=request.POST['process_name'].strip(), long_name=request.POST['long_name'], description=request.POST['help_text'],process_image=file_name,active_flag=role_act,last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    rp.save()
                    add_dashboard_in_process(assign_dashboard['assign_dashboard'],rp.id,request.user.user_id)
                    json_data = json.dumps( { 'process': get_process() , 'status': 'success'} )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )
            else:
                chk=AvMasterProcess.objects.filter(short_name=request.POST['process_name'].strip()).exclude(id=request.POST['process_id'])
                if  len(chk)==0:
                    AvMasterProcess.objects.filter(id=request.POST['process_id']).update(short_name=request.POST['process_name'].strip(), long_name=request.POST['long_name'], description=request.POST['help_text'],process_image=file_name,active_flag=role_act,last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    add_dashboard_in_process(assign_dashboard['assign_dashboard'],request.POST['process_id'],request.user.user_id)
                    json_data = json.dumps( { 'process': get_process() , 'status': 'success'} )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )

    else:
        json_data = json.dumps( { 'process': get_process(), 'dashboard': list(dashboard) , 'rolePermission':rolePermission } )

    return HttpResponse( json_data , content_type='application/json')



def get_process():
    process=AvMasterProcess.objects.order_by('id')
    process_json = serializers.serialize('json', process )
    data_process_json = json.loads( process_json )
    return data_process_json


@csrf_exempt
def processStatus(request):
    process_id=list(request.POST)
    process_id=int(''.join(map(str,process_id)))
    stat=AvMasterProcess.objects.values('active_flag').filter(id=process_id)
    if stat[0]['active_flag']=='Y':
        status='N'
        msg='No'
    else:
        status='Y'
        msg='Yes'

    AvMasterProcess.objects.filter(id=process_id).update(active_flag=status,last_updated_by=request.user.user_id,last_updated_date=datetime.now())

    json_data = json.dumps( {'status': 'success' , 'msg':msg , 'update_by':request.user.user_id} )
    return HttpResponse( json_data , content_type='application/json' )



def add_dashboard_in_process(dashboards,process_id,uID):
    AvMasterProcessDashboards.objects.filter(process_id=process_id).delete()
    for p in dashboards:
        dash=p.split(',')
        for d in dash:
            dat=AvMasterDashboard.objects.values('id','short_name').filter(id=d)
            s=AvMasterProcessDashboards(process_id=process_id,dashboard_id=dat[0]['id'],active_flag='Y',last_updated_date=datetime.now(),last_updated_by=uID)
            s.save()


@csrf_exempt
def process_edit(request):
    process_id=list(request.POST)
    process_id=int(''.join(map(str,process_id)))

    process=AvMasterProcess.objects.filter(id=process_id)
    process_json = serializers.serialize('json', process )
    Data_process_json = json.loads( process_json )

    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)

    dashboard=AvMasterDashboard.objects.values('id','short_name').filter(active_flag='Y').order_by('id')
    user_dashboard=AvMasterProcessDashboards.objects.values('dashboard_id','process_id').filter(process_id=process_id)

    user_added_dashboard=[]
    userP=[]
    for user_dash in user_dashboard:
        dash=AvMasterDashboard.objects.values('short_name').filter(id=user_dash['dashboard_id'])
        userP.append(user_dash['dashboard_id'])
        user_added_dashboard.append([user_dash['dashboard_id'],dash[0]['short_name']])

    dashboardD = []
    for master_dash in dashboard:
        if master_dash['id'] not in userP:
            dashboardD.append([master_dash['id'],master_dash['short_name']])

    json_data = json.dumps( {'status': 'success' , 'process':Data_process_json, 'user_added_dashboard': list(user_added_dashboard) , 'dashboardData':dashboardD , 'rolePermission':rolePermission } )
    return HttpResponse( json_data , content_type='application/json' )
