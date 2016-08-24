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
def uploadEmployeeData(request):
    json_data=None
    DataType=AvMasterUploadDataType.objects.order_by('data_type')
    DataType_json = serializers.serialize('json', DataType )
    DataType_json_list = json.loads( DataType_json )
    cursor = connection.cursor()
    
    rolePermisn=utilb.userRolePermission(request.user.company.id,request.user.user_id)
    compData=''

    if 'View All Companies' in rolePermisn:
        compData=AvMasterCompany.objects.values('id','short_name').order_by('short_name')
    elif 'View Company' in rolePermisn:
        compData=AvMasterCompany.objects.values('id','short_name').filter(id=request.user.company.id).order_by('short_name')

    if request.method == "POST":
        data=request.FILES['file']
        path = default_storage.save('tmp/import.xls', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        records = pe.get_records(file_name=tmp_file)
        req=request.POST

        cursor.execute("SELECT nextval('av_log_data_upload_id_seq')")
        upload_id=cursor.fetchone()
        cursor.close()
        uploadID=int(''.join(map(str,upload_id)))

        c=AvLogDataUploads(data_upload_id=uploadID,company_id=request.user.company.id,company_name=request.user.company.short_name,data_type=req['data_type'],uploaded_by=request.user.user_id,uploaded_date=datetime.now(),no_of_records='0',status='1 of 6 - File Upload',upload_or_rollback='File Upload')
        c.save()

        json_data = json.dumps( { 'status':'success','message':'File uploaded successfully.', 'file_name':tmp_file, 'upload_id':uploadID ,'logData': getLogData(request.user.company.id) } )
        utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'Data Load','Load Start','Information','File Uploaded',request.user.user_id,uploadID,'uploadData')

    else:
        json_data = json.dumps( { 'DataType':DataType_json_list, 'compData':list(compData) ,'UserCompId':request.user.company.id, 'logData': getLogData(request.user.company.id), 'rolePermission':utilb.userRolePermission(request.user.company.id,request.user.user_id)} )

    return HttpResponse( json_data , content_type='application/json')



@csrf_exempt
def upload_employeedata_step2(request):
    req=request.POST
    records = pe.get_records(file_name=req['file_name'])

    if ('Employee ID' in records[0] and req['data_type']=='Employee') or  ('Report ID' in records[0] and req['data_type']=='Expenses'):
        json_data = json.dumps( { 'status':'success','message':'File formate is ok.', 'file_name':req['file_name'], 'upload_id':req['upload_id']  } )
        AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(status='2 of 6 File Formate Check')
        utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'Data Load','Records Processed','Information','Checked file formate',request.user.user_id,req['upload_id'],'uploadData')
    else:
        json_data = json.dumps( { 'status':'danger','message':'File formate is not valid.', 'file_name':req['file_name'], 'upload_id':req['upload_id']  } )
        AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(status='1 of 6 File Formate Check')
        utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'Data Load','Records Processed','Information','Checked file formate failed',request.user.user_id,req['upload_id'],'uploadData')
    return HttpResponse( json_data , content_type='application/json')



@csrf_exempt
def upload_employeedata_step3(request):
    req=request.POST
    records = pe.get_records(file_name=req['file_name'])

    stat=True
    if req['data_type']=='Employee':
        ls=[]
        for record in records:
            if record['Employee ID'] in ls:
                stat=False
            ls.append(record['Employee ID'])

    elif req['data_type']=='Expenses':
        ls=[]
        for record in records:
            if record['Report Line ID'] in ls:
                stat=False
            ls.append(record['Report Line ID'])


    if stat==True:
        status='success'
        msg='All records is unique'
        AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(status='4 of 6 File Formate Check')
        utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'Data Load','Duplicate Records','Information','Duplicate Records checked',request.user.user_id,req['upload_id'],'uploadData')
    else:
        status='danger'
        msg='Some records are duplicate'
        AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(status='2 of 6 File Formate Check')
        utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'Data Load','Duplicate Records','Information','Duplicate Records checked failed',request.user.user_id,req['upload_id'],'uploadData')

    json_data = json.dumps( { 'status':status,'message':msg, 'file_name':req['file_name'], 'upload_id':req['upload_id']  } )
    return HttpResponse( json_data , content_type='application/json')




@csrf_exempt
def upload_employeedata_step5(request):
    req=request.POST
    records = pe.get_records(file_name=req['file_name'])

    chk=insertData(records,req,request.user.user_id,req['file_name'])
    stat=None
    if req['data_type']=='Employee':
        sqlqry="SELECT av_engine.av_trxn_company_employees_load_fn(%s, '%s', '%s','%s')"%(req['comp_id'],req['comp_name'],request.user.user_id,req['upload_id'])
        ret_msg=custom_query(sqlqry)
        if ret_msg=='SUCCESS':
            stat='success'
            AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(no_of_records=chk,status='5 to 6 Master Updates Done',upload_or_rollback='Upload to Rollback')
        else:
            AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(no_of_records=chk,status='5 to 6 Master Updates Error',upload_or_rollback='Upload to Rollback')
            stat='error'
    elif req['data_type']=='Expenses':
        sqlqry="SELECT av_engine.av_trxn_expenses_load_fn(%s, '%s', '%s','%s')"%(req['comp_id'],req['comp_name'],request.user.user_id,req['upload_id'])
        ret_msg=custom_query(sqlqry)
        if ret_msg=='SUCCESS':
            stat='success'
            AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(no_of_records=chk,status='5 to 6 Master Updates Done',upload_or_rollback='Upload to Rollback')
        else:
            stat='error'
            AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(no_of_records=chk,status='5 to 6 Master Updates Error',upload_or_rollback='Upload to Rollback')

    json_data = json.dumps( { 'status':stat,'message':'All records successfully inserted', 'chk':chk, 'file_name':req['file_name'], 'upload_id':req['upload_id']  } )
    utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'Data Load','Records Inserted','Information','Records Inserted',request.user.user_id,req['upload_id'],'uploadData')
    return HttpResponse( json_data , content_type='application/json')

@csrf_exempt
def upload_employeedata_step6(request):
    req=request.POST
    records = pe.get_records(file_name=req['file_name'])

    if req['data_type']=='Employee':
        AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(status='6 of 6 Audvantage Done')
        msg='6 to 6 Audvantage Done'
    elif req['data_type']=='Expenses':
        sqlqry="SELECT av_engine.av_check_exp_engine_fn(%s, '%s', '%s','%s')"%(req['comp_id'],req['comp_name'],request.user.user_id,req['upload_id'])
        ret_msg=custom_query(sqlqry)
        if ret_msg=='SUCCESS':
            msg='6 to 6 Audvantage Done'
            AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(status='6 of 6 Audvantage Done')
        else:
            AvLogDataUploads.objects.filter(data_upload_id=req['upload_id']).update(status='6 of 6 Audvantage Error')
            msg='6 to 6 Audvantage Error'

    json_data = json.dumps( { 'status':'success','message':msg, 'file_name':req['file_name'], 'upload_id':req['upload_id'] , 'logData': getLogData(request.user.company.id) } )
    utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'Data Load','Load End','Information','Load End',request.user.user_id,req['upload_id'],'uploadData')
    return HttpResponse( json_data , content_type='application/json')


def insertData(dat,ps,uId,file_name):
    if ps['data_type']=='Employee':
        AvTrxnCompanyEmployeesS.objects.filter(company_id=ps['comp_id']).delete()
        tot=0
        for record in dat:
            try:
                tot+=1
                p=AvTrxnCompanyEmployeesS(data_upload_id=ps['upload_id'],company_id=ps['comp_id'],employee_id=record['Employee ID'],employee_number=record['Employee Number'],employee_email=record['Employee Email'],first_name=record['First Name'],last_name=record['Last Name'],nick_name=record['Nick Name'],start_date=record['Start Date'],end_date=record['End Date'],assignment_status=record['Assignment Status'],job_title=record['Job Title'],department_code=record['Department Code'],department_name=record['Department Name'],function_name=record['Function Name'],location_name=record['Location'],country=record['Country'],manager_employee_number=record['Manager Employee Number'],active_flag=record['Active (Y/N)'],last_updated_date=record['Last Updated Date'],last_updated_by=record['Last Updated By'],record_insert_date=datetime.now(),record_insert_by=uId,custom_field1=record['Custom Field1'],custom_field2=record['Custom Field2'],custom_field3=record['Custom Field3'],custom_field4=record['Custom Field4'],custom_field5=record['Custom Field5'])
                p.save()
            except Exception as e:
                tot-=1
                print 'Error'

        return tot

    elif ps['data_type']=='Expenses':
        AvTrxnExpExpensesS.objects.filter(company_id=ps['comp_id']).delete()
        tot=0
        for record in dat:
            try:
                tot+=1
                p=AvTrxnExpExpensesS(data_upload_id=ps['upload_id'],source_system=record['Source System'],company_id=ps['comp_id'],report_id=record['Report ID'],report_line_id=record['Report Line ID'],report_owner_id=record['Report Owner ID'],expense_type_code=record['Expense Type Code'],expense_type_name=record['Expense Type Name'],spend_category_code=record['Spend Category Code'],spend_category_name=record['Spend Category Name'],payment_type_id=record['Payment Type ID'],payment_type_name=record['Payment Type Name'],transaction_date=record['Transaction Date'],transaction_currency_code=record['Transaction Currency Code'],transaction_amount=record['Transaction Amount'],exchange_rate=record['Exchange Rate'],posted_amount=record['Posted Amount'],approved_amount=record['Approved Amount'],vendor_description=record['Vendor Description'],vendor_list_item_id=record['Vendor List Item ID'],vendor_list_item_name=record['Vendor List Item Name'],location_id=record['Location ID'],location_name=record['Location Name'],location_subdivision=record['Location Subdivision'],location_country=record['Location Country'],description=record['Description'],is_personal=record['Is Personal'],is_billable=record['Is Billable'],is_personal_card_charge=record['Is Personal Card Charge'],has_image=record['HasImage'],is_image_required=record['IsImageRequired'],receipt_received=record['Receipt Received'],tax_receipt_type=record['Tax Receipt Type'],electronic_receipt_id=record['Electronic Receipt ID'],company_card_transaction_id=record['Company Card Transaction ID'],trip_id=record['Trip ID'],has_itemizations=record['Has Itemizations'],allocation_type=record['AllocationType'],has_attendees=record['Has Attendees'],has_vat=record['Has VAT'],has_applied_cash_advance=record['Has Applied Cash Advance'],has_comments=record['Has Comments'],has_exceptions=record['Has Exceptions'],is_paid_by_expense_pay=record['Is Paid By Expense Pay'],employee_bank_account_id=record['Employee Bank Account ID'],journey=record['Journey'],last_modified=record['Last Modified'],last_modified_by=record['Last Modified By'],org_unit=record['Org Unit'],record_insert_date=datetime.now(),record_insert_by=uId,custom_field1=record['Custom Field1'],custom_field2=record['Custom Field2'],custom_field3=record['Custom Field3'],custom_field4=record['Custom Field4'],custom_field5=record['Custom Field5'])
                p.save()
            except Exception as e:
                print 'Error'

        return tot

    elif ps['data_type']=='Invoices':
        for record in dat:
            print ''

    elif ps['data_type']=='Payments':
        for record in dat:
            print ''

    elif ps['data_type']=='Purchase Orders':
        for record in dat:
            print ''


@csrf_exempt
def get_data_log(request):
    req=list(request.POST)
    uploadID=int(''.join(map(str,req)))
    Log=AvLogAuditTrail.objects.filter(company_id=request.user.company.id,object_id=uploadID).order_by('event_date')
    LogData_json = serializers.serialize('json', Log )
    LogData_json_list = json.loads( LogData_json )
    json_data = json.dumps( { 'status':'success', 'log':LogData_json_list } )
    return HttpResponse( json_data , content_type='application/json')




def getLogData(comp_id):
    LogData=AvLogDataUploads.objects.filter(company_id=comp_id).order_by('-uploaded_date')
    LogData_json = serializers.serialize('json', LogData )
    LogData_json_list = json.loads( LogData_json )
    return LogData_json_list



@csrf_exempt
def data_rollback(request):
    post_data=list(request.POST)
    post_data=str(''.join(map(str,post_data)))
    post_data=post_data.split('-')
    dataType=post_data[0]
    upload_id=post_data[1]

    upload_id=int(''.join(map(str,upload_id)))
    AvLogDataUploads.objects.filter(data_upload_id=upload_id).update(status='1 of 3 Rollback In Progress')
    json_data = json.dumps( { 'status':'success','message':'1 of 3 Rollback In Progress'} )
    utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Rollback','Information','Start',request.user.user_id,'1','Data Rollback Start')
    return HttpResponse( json_data , content_type='application/json')


@csrf_exempt
def data_rollback2(request):
    post_data=list(request.POST)
    post_data=str(''.join(map(str,post_data)))
    post_data=post_data.split('-')
    dataType=post_data[0]
    upload_id=post_data[1]

    upload_id=int(''.join(map(str,upload_id)))
    if dataType=='Expenses':
        qry="SELECT av_engine.av_trxn_expenses_rollback_fn(%s, '%s', '%s', %s)"%(request.user.company_id,request.user.company.short_name,request.user.user_id,upload_id)
    else:
        qry="SELECT av_engine.av_trxn_company_employees_rollback_fn(%s, '%s', '%s', %s)"%(request.user.company_id,request.user.company.short_name,request.user.user_id,upload_id)

    utilb.customQryExc(qry)

    AvLogDataUploads.objects.filter(data_upload_id=upload_id).update(status='2 of 3 Master Updates In Progress')
    json_data = json.dumps( { 'status':'success','message':'2 of 3 Master Updates In Progress'} )
    utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Rollback','Information','Progress',request.user.user_id,'1','Data Rollback In Progress')
    return HttpResponse( json_data , content_type='application/json')


@csrf_exempt
def data_rollback3(request):
    post_data=list(request.POST)
    post_data=str(''.join(map(str,post_data)))
    post_data=post_data.split('-')
    dataType=post_data[0]
    upload_id=post_data[1]

    upload_id=int(''.join(map(str,upload_id)))
    qry="SELECT av_engine.av_check_exp_engine_fn(%s, '%s', '%s', %s)"%(request.user.company_id,request.user.company.short_name,request.user.user_id,upload_id)
    utilb.customQryExc(qry)

    AvLogDataUploads.objects.filter(data_upload_id=upload_id).update(status='3 of 3 Rollback Done', upload_or_rollback='Rollbacked')
    json_data = json.dumps( { 'status':'success','message':'3 of 3 Rollback Done'} )
    utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Rollback','Information','Done',request.user.user_id,'1','Data Rollback Done')
    return HttpResponse( json_data , content_type='application/json')


@csrf_exempt
def auditlog(request):
    json_data=None
    if request.method == "POST":
        reqdata=dict(request.POST)
        if 'comp_name' or 'event_category' or 'user' or 'start_date' or 'event_sub_category' or 'keyword' or 'end_date' or 'event_type'  in reqdata and (reqdata['comp_name']!=[''] or reqdata['event_category']!=[''] or reqdata['user']!=[''] or reqdata['start_date']!=[''] or reqdata['event_sub_category']!=[''] or reqdata['keyword']!=[''] or reqdata['end_date']!=[''] or reqdata['event_type']!=[''] ):

            if 'comp_name' in reqdata and reqdata['comp_name']!=['']:
                compID=int(''.join(map(str,reqdata['comp_name'])))
                SqlQuery=Q(company_id=compID )

            if 'event_category' in reqdata and reqdata['event_category']!=['']:
                SqlQuery &= Q(event_category__in=reqdata['event_category'] )

            if 'user' in reqdata and reqdata['user']!=['']:
                userName=''.join(map(str, reqdata['user']))
                SqlQuery &= Q(event_user__icontains=userName.strip())

            if 'start_date' and 'end_date' in reqdata and (reqdata['start_date']!=[''] and reqdata['end_date']!=['']):
                start_date=''.join(map(str, reqdata['start_date']))
                end_date=''.join(map(str, reqdata['end_date']))
                SqlQuery &= Q(event_date__range=[start_date,end_date] )


            if 'start_date' in reqdata and reqdata['start_date']!=[''] and reqdata['end_date']==['']:
                start_date=''.join(map(str, reqdata['start_date']))
                SqlQuery &= Q(event_date__date=start_date)


            if 'event_sub_category' in reqdata and reqdata['event_sub_category']!=['']:
                SqlQuery &= Q(event_sub_category__in=reqdata['event_sub_category'] )

            if 'event_type' in reqdata and reqdata['event_type']!=['']:
                SqlQuery &= Q(event_type__in=reqdata['event_type'] )

            # if 'keyword' in reqdata and reqdata['keyword']!=['']:
            #     dta_keyword=''.join(map(str, reqdata['keyword']))
            #     SqlQuery &= Q(event_user__icontains=dta_keyword.strip())


            LogData = AvLogAuditTrail.objects.filter( SqlQuery ).order_by("-event_date")
            expt_file_name=utilb.export_auditlog(LogData)
            LogData_json = serializers.serialize('json', LogData )
            LogData_json_list = json.loads( LogData_json )
            json_data = json.dumps( { 'logData':LogData_json_list, 'expt_file_name':expt_file_name } )
            utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Audit Log','Information','Audit Log',request.user.user_id,'1','Search data')

        else:
            print 'No- data'

    else:
        rolePermisn=utilb.userRolePermission(request.user.company.id,request.user.user_id)
        compData=''
        if 'View All Companies' in rolePermisn:
            compData=AvMasterCompany.objects.values('id','short_name').order_by('short_name')
        elif 'View Company' in rolePermisn:
            compData=AvMasterCompany.objects.values('id','short_name').filter(id=request.user.company.id).order_by('short_name')


        eventCategory=AvMasterEvents.objects.values('event_category').annotate(event_category_name=Count('event_category')).order_by('event_category')
        eventType=AvMasterEvents.objects.values('event_type').annotate(event_type_name=Count('event_type')).order_by('event_type')

        json_data = json.dumps( { 'compData':list(compData) ,'UserCompId':request.user.company.id, 'eventCategory':list(eventCategory) , 'eventSubCategory':'', 'eventType': list(eventType), 'rolePermission':utilb.userRolePermission(request.user.company.id,request.user.user_id)} )
        utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Audit Log','Information','Audit Log',request.user.user_id,'1','Visiting on page')
    return HttpResponse( json_data , content_type='application/json')



@csrf_exempt
def get_eventsubcategory(request):
    post_data=list(request.POST)
    post_data=str(''.join(map(str,post_data)))
    subcat=AvMasterEvents.objects.values('event_sub_category').annotate(subCat=Count('event_sub_category')).filter(event_category=post_data).order_by('event_sub_category')
    json_data = json.dumps( { 'subCategory':list(subcat) } )
    return HttpResponse( json_data , content_type='application/json')


def delfile(request):
    filn=request.session['file_name']
    print filn
    if os.path.isfile(filn):
        os.remove(filn)
        del request.session['file_name']

    filn=request.session['file_name']
    json_data = json.dumps( { 'file_name':filn} )
    return HttpResponse( json_data , content_type='application/json')


def custom_query(qry):
    cursor = connection.cursor()
    cursor.execute(qry)
    upload_id=cursor.fetchone()
    cursor.close()
    ret=list(upload_id)
    return str(''.join(map(str,ret)))
