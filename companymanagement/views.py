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
def companyIndex(request):
    json_data=None
    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)
    dashboard=AvMasterDashboard.objects.values('id','short_name').filter(active_flag='Y').order_by('id')

    if request.method == "POST":
        if request.POST['short_name']!='' and request.POST['full_name']!='' and request.POST['address1']!='':

            if 'file' in request.FILES and request.FILES['file']!=[]:
                file_name = str(int(round(time.time() * 1000)))+'-'+str(request.FILES['file'])
                path = default_storage.save('static/uploaded/'+file_name, ContentFile(request.FILES['file'].read()))
            else:
                file_name=request.POST['edit_pic_name']

            if request.POST['company_id']=='':
                chk=AvMasterCompany.objects.filter(short_name=request.POST['short_name'].strip())
                if  len(chk)==0:
                    rp=AvMasterCompany(short_name=request.POST['short_name'].strip(), full_name=request.POST['full_name'], address1=request.POST['address1'],logo=file_name,active_flag=request.POST['active_flag'],address2=request.POST['address2'],city=request.POST['city'],state=request.POST['state'],country=request.POST['country'],zip_code=request.POST['zip_code'],primary_contact_name=request.POST['primary_contact_name'],primary_contact_email=request.POST['primary_contact_email'],primary_contact_phone=request.POST['primary_contact_phone'],secondary_contact_name=request.POST['secondary_contact_name'],secondary_contact_email=request.POST['secondary_contact_email'],secondary_contact_phone=request.POST['secondary_contact_phone'],landing_page_text=request.POST['landing_page_text'],single_sign_on_flag=request.POST['single_sign_on_flag'],last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    rp.save()
                    insert_process_in_company(rp.id,request.user.user_id)
                    json_data = json.dumps( { 'company': get_company() , 'status': 'success'} )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )
            else:
                chk=AvMasterCompany.objects.filter(short_name=request.POST['short_name'].strip()).exclude(id=request.POST['company_id'])
                if  len(chk)==0:
                    AvMasterCompany.objects.filter(id=request.POST['company_id']).update(short_name=request.POST['short_name'].strip(), full_name=request.POST['full_name'], address1=request.POST['address1'],logo=file_name,active_flag=request.POST['active_flag'],address2=request.POST['address2'],city=request.POST['city'],state=request.POST['state'],country=request.POST['country'],zip_code=request.POST['zip_code'],primary_contact_name=request.POST['primary_contact_name'],primary_contact_email=request.POST['primary_contact_email'],primary_contact_phone=request.POST['primary_contact_phone'],secondary_contact_name=request.POST['secondary_contact_name'],secondary_contact_email=request.POST['secondary_contact_email'],secondary_contact_phone=request.POST['secondary_contact_phone'],landing_page_text=request.POST['landing_page_text'],single_sign_on_flag=request.POST['single_sign_on_flag'],last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    json_data = json.dumps( { 'company': get_company() , 'status': 'success'} )
                else:
                    json_data = json.dumps( { 'status': 'danger'} )

    else:
        json_data = json.dumps( { 'company': get_company(), 'dashboard': 'list(dashboard)' , 'rolePermission':rolePermission } )

    return HttpResponse( json_data , content_type='application/json')



def get_company():
    company=AvMasterCompany.objects.order_by('id')
    company_json = serializers.serialize('json', company )
    data_company_json = json.loads( company_json )
    return data_company_json


def insert_process_in_company(compId,updateBy):
    process=AvMasterProcess.objects.values('id','short_name').filter(active_flag='Y')
    for proc in process:
        rp=AvMasterCompanyProcess(company_id=compId, process_id=proc['id'], no_of_licenses='0',active_flag='Y',last_updated_by=updateBy,last_updated_date=datetime.now())
        rp.save()


@csrf_exempt
def companyStatus(request):
    company_id=list(request.POST)
    company_id=int(''.join(map(str,company_id)))
    stat=AvMasterCompany.objects.values('active_flag').filter(id=company_id)
    if stat[0]['active_flag']=='Y':
        status='N'
        msg='No'
    else:
        status='Y'
        msg='Yes'

    AvMasterCompany.objects.filter(id=company_id).update(active_flag=status,last_updated_by=request.user.user_id,last_updated_date=datetime.now())

    json_data = json.dumps( {'status': 'success' , 'msg':msg,'update_by':request.user.user_id} )
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
def company_edit(request):
    company_id=list(request.POST)
    company_id=int(''.join(map(str,company_id)))

    company=AvMasterCompany.objects.filter(id=company_id)
    company_json = serializers.serialize('json', company )
    Data_company_json = json.loads( company_json )

    json_data = json.dumps( {'status': 'success' , 'company':Data_company_json } )
    return HttpResponse( json_data , content_type='application/json' )


@csrf_exempt
def company_licenses(request):
    from bson import json_util
    company_id=list(request.POST)
    company_id=str(''.join(map(str,company_id)))

    qry="select mp.short_name as process_name,mcp.* from av_master_company_process as mcp left join av_master_process as mp on mcp.process_id=mp.id where company_id='%s'"%(company_id)
    dat=utilb.customQryExc(qry)

    company=AvMasterCompany.objects.values('id','short_name','full_name').filter(id=company_id)
    json_data = json.dumps( {'status': 'success' , 'compnay_licenses': dat , 'company_data':list(company) } , default=json_util.default )
    return HttpResponse( json_data , content_type='application/json' )


@csrf_exempt
def update_company_licenses(request):
    chk=AvMasterCompanyProcess.objects.filter(no_of_licenses=request.POST['license'].strip()).exclude(id=request.POST['comp_process_id'])
    if  len(chk)==0:
        AvMasterCompanyProcess.objects.filter(id=request.POST['comp_process_id']).update(no_of_licenses=request.POST['license'],last_updated_by=request.user.user_id,last_updated_date=datetime.now())
        json_data = json.dumps( {'status': 'success' } )
    else:
        json_data = json.dumps( { 'status': 'danger'} )

    return HttpResponse( json_data , content_type='application/json' )


@csrf_exempt
def company_dashboards(request):
    company_id=list(request.POST)
    company_id=str(''.join(map(str,company_id)))

    company=AvMasterCompany.objects.values('id','short_name','full_name').filter(id=company_id)

    dashboards = AvMasterProcessDashboards.objects.values('dashboard_id').annotate(dashboard=Count('dashboard_id'))
    #dashboards = AvMasterDashboard.objects.values('id','short_name').filter(active_flag='Y').order_by('id')
    qry="SELECT mcpd.dashboard_id,md.short_name FROM av_master_company_process_dashboards as mcpd left join av_master_dashboard as md on mcpd.dashboard_id=md.id where mcpd.company_id='%s'"%(company_id)
    asigned_dashboard=utilb.customQryExc(qry)

    userDash=[]
    for user_d in asigned_dashboard:
        userDash.append(user_d[0])

    available_dashboards = []
    for master_dash in dashboards:
        if master_dash['dashboard_id'] not in userDash:
            dash=AvMasterDashboard.objects.values('short_name').filter(id=master_dash['dashboard_id'])
            available_dashboards.append([master_dash['dashboard_id'],dash[0]['short_name']])

    json_data = json.dumps( {'status': 'success' , 'company_data':list(company) , 'asigned_dashboard':asigned_dashboard, 'available_dashboards':available_dashboards } )
    return HttpResponse( json_data , content_type='application/json' )



@csrf_exempt
def update_company_dashboard(request):
    AvMasterCompanyProcessDashboards.objects.filter(company_id=request.POST['company_id']).delete()
    import ast
    dashboards = ast.literal_eval(request.POST['assigned_dashboard'])
    if type(dashboards) is int:
        dat=AvMasterProcessDashboards.objects.values('process_id','dashboard_id').filter(dashboard_id=dashboards)
        s=AvMasterCompanyProcessDashboards(company_id=request.POST['company_id'],process_id=dat[0]['process_id'],dashboard_id=dat[0]['dashboard_id'],active_flag='Y',last_updated_date=datetime.now(),last_updated_by=request.user.user_id)
        s.save()
    else:
        for dash_id in dashboards:
            dat=AvMasterProcessDashboards.objects.values('process_id','dashboard_id').filter(dashboard_id=dash_id)
            s=AvMasterCompanyProcessDashboards(company_id=request.POST['company_id'],process_id=dat[0]['process_id'],dashboard_id=dat[0]['dashboard_id'],active_flag='Y',last_updated_date=datetime.now(),last_updated_by=request.user.user_id)
            s.save()

    json_data = json.dumps( {'status': 'success' } )
    return HttpResponse( json_data , content_type='application/json' )
