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
def messageIndex(request):
    from bson import json_util
    json_data=None
    rolePermission=utilb.userRolePermission(request.user.company.id,request.user.user_id)
    compData=''
    if 'View All Companies' in rolePermission:
        compData=AvMasterCompany.objects.values('id','short_name').filter(active_flag='Y').order_by('short_name')
    elif 'View Company' in rolePermisn:
        compData=AvMasterCompany.objects.values('id','short_name').filter(id=request.user.company.id).order_by('short_name')


    if request.method == "POST":
        print request.POST
        if request.POST['company_name']!='' and request.POST['message_text']!='':
            if request.POST['message_id']=='':
                if request.POST['message_type']=='C':
                    rp=AvMasterCompanyMessage(company_id=request.POST['company_name'], message_type=request.POST['message_type'], message_text=request.POST['message_text'].strip(),active_flag=request.POST['active_flag'],last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    rp.save()
                else:
                    rp=AvMasterCompanyMessage(message_type=request.POST['message_type'], message_text=request.POST['message_text'].strip(),active_flag='Y',last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                    rp.save()
                json_data = json.dumps( { 'messages': get_message() , 'status': 'success'} , default=json_util.default)
            else:
                AvMasterCompanyMessage.objects.filter(id=request.POST['message_id']).update(message_text=request.POST['message_text'].strip(),last_updated_by=request.user.user_id,last_updated_date=datetime.now())
                json_data = json.dumps( { 'messages': get_message() , 'status': 'success'} , default=json_util.default)
    else:
        json_data = json.dumps( { 'messages': get_message(), 'compData':list(compData), 'UserCompId':request.user.company.id , 'rolePermission':rolePermission } , default=json_util.default )

    return HttpResponse( json_data , content_type='application/json')



def get_message():
    company_message=AvMasterCompanyMessage.objects.order_by('-id')

    messages=defaultdict(list)
    ct=0
    for cm in company_message:
        company_name='System'
        if cm.company_id !=None:
            company=AvMasterCompany.objects.values('short_name').filter(id=cm.company_id)
            company_name=company[0]['short_name']

        messages[ct].append([cm.id,cm.company_id,company_name,cm.message_type,cm.message_text,cm.active_flag,cm.last_updated_by,cm.last_updated_date])
        ct += 1

    return messages


@csrf_exempt
def messageStatus(request):
    message_id=list(request.POST)
    message_id=int(''.join(map(str,message_id)))
    stat=AvMasterCompanyMessage.objects.values('active_flag').filter(id=message_id)
    if stat[0]['active_flag']=='Y':
        status='N'
        msg='No'
    else:
        status='Y'
        msg='Yes'

    AvMasterCompanyMessage.objects.filter(id=message_id).update(active_flag=status,last_updated_by=request.user.user_id,last_updated_date=datetime.now())

    json_data = json.dumps( {'status': 'success' , 'msg':msg,'update_by':request.user.user_id} )
    return HttpResponse( json_data , content_type='application/json' )


@csrf_exempt
def message_edit(request):
    message_id=list(request.POST)
    message_id=int(''.join(map(str,message_id)))

    message=AvMasterCompanyMessage.objects.filter(id=message_id)
    message_json = serializers.serialize('json', message )
    Data_message_json = json.loads( message_json )

    json_data = json.dumps( {'status': 'success' , 'message':Data_message_json } )
    return HttpResponse( json_data , content_type='application/json' )
