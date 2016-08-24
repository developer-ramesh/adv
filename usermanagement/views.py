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
from passlib.hash import django_salted_sha1 as handler


@csrf_exempt
def userIndex(request):
    from bson import json_util
    json_data=None
    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)
    compData=''
    if 'View All Companies' in rolePermission:
        compData=AvMasterCompany.objects.values('id','short_name').filter(active_flag='Y').order_by('short_name')
    elif 'View Company' in rolePermisn:
        compData=AvMasterCompany.objects.values('id','short_name').filter(id=request.user.company.id).order_by('short_name')

    if request.method == "POST":
        if request.POST['company_id']!='' and request.POST['user_name']!='':
            if request.POST['user_id']=='':
                chk=AvMasterCompanyUsers.objects.filter(user_id=request.POST['user_name'].strip())
                if  len(chk)==0:
                    last_id = AvMasterCompanyUsers.objects.last()
                    passwd = handler.encrypt(request.POST['password'].strip())
                    rp=AvMasterCompanyUsers(id=last_id.id+1,user_id=request.POST['user_name'].strip(), company_id=request.POST['company_id'], password=passwd, first_name=request.POST['fisrt_name'],last_name=request.POST['last_name'],nick_name=request.POST['nice_name'],email_address=request.POST['email'],employee_number='0',active_flag=request.POST['active_flag'],last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    rp.save()
                    json_data = json.dumps( { 'users': get_user() , 'status': 'success'} , default=json_util.default )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )
            else:
                chk=AvMasterCompanyUsers.objects.filter(user_id=request.POST['user_name'].strip()).exclude(id=request.POST['user_id'])
                if  len(chk)==0:
                    AvMasterCompanyUsers.objects.filter(id=request.POST['user_id']).update(user_id=request.POST['user_name'].strip(), company_id=request.POST['company_id'], first_name=request.POST['fisrt_name'],last_name=request.POST['last_name'],nick_name=request.POST['nice_name'],email_address=request.POST['email'],active_flag=request.POST['active_flag'],last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    json_data = json.dumps( { 'users': get_user() , 'status': 'success'} , default=json_util.default )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )
    else:
        json_data = json.dumps( { 'users': get_user(), 'compData':list(compData), 'UserCompId':request.user.company.id , 'rolePermission':rolePermission } , default=json_util.default )

    return HttpResponse( json_data , content_type='application/json')



def get_user():
    users=AvMasterCompanyUsers.objects.order_by('-id')
    user_data=defaultdict(list)
    ct=0
    for usr in users:
        user_data[ct].append([usr.id,usr.company_id,usr.company.short_name,usr.user_id,usr.first_name,usr.last_name,usr.email_address,usr.active_flag,usr.last_updated_by,usr.last_updated_date])
        ct += 1

    return user_data


@csrf_exempt
def userStatus(request):
    user_id=list(request.POST)
    user_id=int(''.join(map(str,user_id)))
    stat=AvMasterCompanyUsers.objects.values('active_flag').filter(id=user_id)
    if stat[0]['active_flag']=='Y':
        status='N'
        msg='No'
    else:
        status='Y'
        msg='Yes'

    AvMasterCompanyUsers.objects.filter(id=user_id).update(active_flag=status,last_updated_by=request.user.user_id,last_updated_date=datetime.now())

    json_data = json.dumps( {'status': 'success' , 'msg':msg,'update_by':request.user.user_id} )
    return HttpResponse( json_data , content_type='application/json' )


@csrf_exempt
def getAssignData(request):
    user_id=request.POST['user_id']

    user_dat=AvMasterCompanyUsers.objects.filter(id=user_id)
    user_data=[user_dat[0].id,user_dat[0].user_id,user_dat[0].email_address,user_dat[0].company.short_name,user_dat[0].company.id]

    user_added_data=[]
    master_data=[]
    if request.POST['assign_type']=='Roles':
        rules = AvMasterRoles.objects.values('id','role_name').filter(active_flag='Y').order_by('id')
        user_rules = AvMasterUserRoles.objects.values('role_id','comments').filter(user_id=user_dat[0].user_id,company_id=user_dat[0].company.id).order_by('id')

        userR=[]
        for user_rule in user_rules:
            userR.append(user_rule['role_id'])
            user_added_data.append([user_rule['role_id'],user_rule['comments']])

        for rule in rules:
            if rule['id'] not in userR:
                master_data.append([rule['id'],rule['role_name']])

    elif request.POST['assign_type']=='Processes':
        process = AvMasterCompanyProcess.objects.filter(company_id=user_dat[0].company.id,active_flag='Y').exclude(no_of_licenses=0).order_by('id')
        print process.query
        user_process = AvMasterUserProcess.objects.values('process_id').filter(user_id=user_dat[0].user_id,company_id=user_dat[0].company.id).order_by('id')
        
        userP=[]
        for user_rule in user_process:
            proce=AvMasterProcess.objects.values('short_name').filter(id=user_rule['process_id'])
            userP.append(user_rule['process_id'])
            user_added_data.append([user_rule['process_id'],proce[0]['short_name']])
        
        for proces in process:
            if proces.process.id not in userP:
                master_data.append([proces.process.id,proces.process.short_name])

    elif request.POST['assign_type']=='Dashboards':
        master_dashboard=utilb.customQryExc("SELECT md.dashboard_id,m.short_name FROM av_master_company_process_dashboards as md left join av_master_dashboard as m on m.id=md.dashboard_id where md.company_id=%s and md.active_flag='Y' GROUP BY md.dashboard_id,m.short_name"%user_dat[0].company.id)
        user_dashboard=utilb.customQryExc("SELECT mud.dashboard_id,m.short_name FROM  av_master_user_process_dashboards as mud left join av_master_dashboard as m on m.id=mud.dashboard_id WHERE user_id='%s' and company_id=%s"%(user_dat[0].user_id,user_dat[0].company.id))
        
        userD=[]
        for user_dash in user_dashboard:
            userD.append(user_dash[0])
            user_added_data.append([user_dash[0],user_dash[1]])
        
        for dash in master_dashboard:
            if dash[0] not in userD:
                master_data.append([dash[0],dash[1]])


    json_data = json.dumps( {'status': 'success' , 'master_data': list(master_data) , 'user_added_data':list(user_added_data) , 'user_data': user_data } )
    return HttpResponse( json_data , content_type='application/json' )



@csrf_exempt
def add_user_assign_data(request):
    dat=''.join(map(str, request.POST['assign_data']))
    dat.split(',')
    roles=list(dat)
    if request.POST['assign_type']=='Roles':
        AvMasterUserRoles.objects.filter(user_id=request.POST['user_id'],company_id=request.POST['company_id']).delete()
        for rd in roles:
            if rd!=',':
                dat=AvMasterRoles.objects.values('id','role_name').filter(id=rd)
                s=AvMasterUserRoles(company_id=request.POST['company_id'],user_id=request.POST['user_id'],role_id=dat[0]['id'],comments=dat[0]['role_name'],active_flag='Y',last_updated_date=datetime.now(),last_updated_by=request.user.user_id)
                s.save()
    elif request.POST['assign_type']=='Processes':
        AvMasterUserProcess.objects.filter(user_id=request.POST['user_id'],company_id=request.POST['company_id']).delete()
        for rd in roles:
            if rd!=',':
                s=AvMasterUserProcess(company_id=request.POST['company_id'],user_id=request.POST['user_id'],process_id=rd,data_scope_flag='N',active_flag='Y',last_updated_date=datetime.now(),last_updated_by=request.user.user_id)
                s.save()
    elif request.POST['assign_type']=='Dashboards':
        AvMasterUserProcessDashboards.objects.filter(user_id=request.POST['user_id'],company_id=request.POST['company_id']).delete()
        for rd in roles:
            if rd!=',':
                dat=AvMasterCompanyProcessDashboards.objects.values('process_id').filter(dashboard_id=rd)
                s=AvMasterUserProcessDashboards(company_id=request.POST['company_id'],user_id=request.POST['user_id'],process_id=dat[0]['process_id'],dashboard_id=rd,active_flag='Y',last_updated_date=datetime.now(),last_updated_by=request.user.user_id)
                s.save()            

    json_data = json.dumps( {'status': 'success'  } )
    return HttpResponse( json_data , content_type='application/json' )
