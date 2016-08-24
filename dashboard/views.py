from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core import serializers
import json
from django.db.models import Sum, Count
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from collections import defaultdict,OrderedDict
from django.template import Context
from django.template.loader import render_to_string, get_template
from datetime import datetime, timedelta
from django.db import connection
import utilb



@csrf_exempt
def getSearchHighDoller(request):
    json_data=None
    if request.method == "POST":
        #reqdata=json.loads(request.body)
        reqdata=dict(request.POST)

        dashboardType=''.join(map(str, reqdata['dashboardType']))
        tbl=get_tbl(reqdata['dashboardType'])

        if 'countryItem' or 'QuarterItem' or 'categoryItem' or 'subCategoryItem' or 'duplicateItem' or 'functionItem' or 'employeeItem' or 'thresholdItem'  in reqdata and (reqdata['countryItem']!=[''] or reqdata['QuarterItem']!=[''] or reqdata['subCategoryItem']!=[''] or reqdata['duplicateItem']!=[''] or reqdata['categoryItem']!=[''] or reqdata['functionItem']!=[''] or reqdata['employeeItem']!=[''] or reqdata['thresholdItem']!=[''] ):
            SqlQuery=Q(company_id=request.user.company_id)

            if 'QuarterItem' in reqdata and reqdata['QuarterItem']!=['']:
                SqlQuery &= Q(c_fiscal_quarter__in=reqdata['QuarterItem'] )

            if 'countryItem' in reqdata and reqdata['countryItem']!=['']:
                SqlQuery &= Q(location_country__in=reqdata['countryItem'] )

            if 'categoryItem' in reqdata and reqdata['categoryItem']!=['']:
                SqlQuery &= Q(expense_type_name__in=reqdata['categoryItem'] )

            if 'subCategoryItem' in reqdata and reqdata['subCategoryItem']!=['']:
                SqlQuery &= Q(spend_category_name__in=reqdata['subCategoryItem'] )

            if 'duplicateItem' in reqdata and reqdata['duplicateItem']!=['']:
                duplicateItem=''.join(map(str, reqdata['duplicateItem']))
                SqlQuery &= Q(c_number_of_duplicates=duplicateItem )

            if 'functionItem' in reqdata and reqdata['functionItem']!=['']:
                SqlQuery &= Q(e_function_name__in=reqdata['functionItem'] )

            if 'employeeItem' in reqdata and reqdata['employeeItem']!=['']:
                employeeItem=''.join(map(str, reqdata['employeeItem']))
                SqlQuery &= Q(e_employee_name__icontains=employeeItem.strip())

            if 'thresholdItem' in reqdata and reqdata['thresholdItem']!=['']:
                thresholdItem=int(''.join(map(str,reqdata['thresholdItem'])))
                SqlQuery &= Q(transaction_amount__gte= thresholdItem )

            if 'start_date' and 'end_date' in reqdata and (reqdata['start_date']!=[''] and reqdata['end_date']!=['']):
                start_date=''.join(map(str, reqdata['start_date']))
                end_date=''.join(map(str, reqdata['end_date']))
                SqlQuery &= Q(transaction_date__range=[start_date,end_date] )

            if 'start_date' in reqdata and reqdata['start_date']!=[''] and reqdata['end_date']==['']:
                start_date=''.join(map(str, reqdata['start_date']))
                SqlQuery &= Q(transaction_date=start_date)


            PDid=utilb.getUserProcessDashboardId(request,dashboardType)
            Dashboard=utilb.userDashboard(request.user.company_id,request.user.user_id, PDid[0], PDid[1])
            ScopeData=AvMasterUserDatascope.objects.values('data_scope_type','company_id', 'process_id').filter(user_id=request.user.user_id, company_id=request.user.company.id , process_id = PDid[0] ).annotate( Count('company_id',distinct=True), Count('process_id',distinct=True), Count('data_scope_type',distinct=True))
            data_scope_flag=str(Dashboard[4])
            rolePerm=utilb.userRolePermission(request.user.company.id,request.user.user_id)

            if 'View All Records' in rolePerm:
                print 'View All Records'

            elif 'View Company Records' in rolePerm:
                if len(Dashboard) >0:
                    if data_scope_flag=='Y':
                        for scope in ScopeData:
                            if scope['data_scope_type']=='Country':
                                SqlQuery &= Q(location_country__in= utilb.getDataScope(request,PDid[0],'Country') )

                            if scope['data_scope_type']=='Hierarchy':
                                 SqlQuery &= Q(e_employee_number__in= utilb.getDataScope(request,PDid[0],'Hierarchy') )

                    else:
                        SqlQuery &= Q(e_employee_number__in= utilb.getDataScope(request,PDid[0],'N') )


            SqlQuery &= Q(process_id=PDid[0], dashboard_id=PDid[1])

            if 'viewBy':
                if 'viewBy' in reqdata and reqdata['viewBy']!=[]:
                    viewBy=''.join(map(str, reqdata['viewBy']))
                    if viewBy=='transaction_amount':
                        minsql=Sum('transaction_amount')
                    else:
                        minsql=Count('report_line_id')
                else:
                    minsql=Sum('transaction_amount')

            Employee = tbl.objects.values('e_employee_name').filter( SqlQuery ).annotate(amount=Sum('transaction_amount'), expenses=Count('report_line_id')).order_by("e_employee_name")
            Department = tbl.objects.values('company_id', 'dashboard_id', 'e_department_name', 'location_country').filter( SqlQuery ).annotate(amount=Sum('transaction_amount'), expenses=Count('report_line_id')).order_by("e_department_name")
            GraphPaymentType = tbl.objects.values('c_month_name','payment_type_name','c_month_id').filter( SqlQuery ).annotate(amount=minsql).order_by("c_month_id")

            payment = defaultdict(list)
            for res in GraphPaymentType:
                payment[res['payment_type_name']].append([res['amount']])

            payment_month = defaultdict(list)
            for res in GraphPaymentType:
                payment_month[res['c_month_id']].append([res['amount']])

            Categories = tbl.objects.values('expense_type_name').filter( SqlQuery ).annotate(category=Count('expense_type_name'),amount=minsql).order_by('expense_type_name')
            GraphCategories = tbl.objects.values('spend_category_name').filter( SqlQuery ).annotate(amount=minsql).order_by("spend_category_name")
            GraphCountries = tbl.objects.values('location_country').filter( SqlQuery ).annotate(amount=minsql).order_by("location_country")
            SearchQuery = tbl.objects.values('company_id','job_id','dashboard_id').filter( SqlQuery ).annotate( total_amount=Sum('transaction_amount'),no_of_exp_reports=Count('report_id',distinct=True), no_of_exp_lines=Count('report_line_id',distinct=True), no_of_employees=Count('report_owner_id',distinct=True), avg_exp_per_report=Sum('transaction_amount')/Count('report_id',distinct=True), avg_exp_per_employee=Sum('transaction_amount')/Count('report_owner_id',distinct=True) )
            BucketAnalysis = tbl.objects.values('job_id','company_id','dashboard_id','c_amount_bucket').filter( SqlQuery ).filter(company_id=request.user.company_id).annotate(expenses=minsql).order_by("expenses")

            QuarterItems = tbl.objects.values('c_fiscal_quarter').filter( SqlQuery ).annotate(category=Count('c_fiscal_quarter')).order_by('c_fiscal_quarter')
            functionItems = tbl.objects.values('e_function_name').filter( SqlQuery ).annotate(category=Count('e_function_name')).order_by('e_function_name')
            json_data = json.dumps( { 'BucketAnalysis':list(BucketAnalysis),'Employee':list(Employee), 'Department':list(Department) , 'GraphMonth':payment , 'PaymentMonth':payment_month, 'GraphCategories':list(GraphCategories) ,'Categories_list':list(Categories), 'GraphCountries':list(GraphCountries) ,'JobStatistics':list(SearchQuery) , 'QuarterItems':list(QuarterItems),'functionItems':list(functionItems) , 'DataType':'search'} )
            utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Filter','Information','Filter',request.user.user_id,'','Expense Duplicate')

        else:
            json_data=getHighDoller(request)
    else:
        json_data=getHighDoller(request)

    return HttpResponse( json_data , content_type='application/json')



def getHighDoller(dat):
    dashboardType=str(dat.GET['dashboardType'])
    tbl=get_tbl(dat.GET['dashboardType'])
    PDid=utilb.getUserProcessDashboardId(dat,dashboardType)
    Dashboard=utilb.userDashboard(dat.user.company_id,dat.user.user_id, PDid[0], PDid[1])
    ScopeData=AvMasterUserDatascope.objects.values('data_scope_type','company_id', 'process_id').filter(user_id=dat.user.user_id, company_id=dat.user.company.id , process_id = PDid[0] ).annotate( Count('company_id',distinct=True), Count('process_id',distinct=True), Count('data_scope_type',distinct=True))

    SqlQuery=Q(company_id=dat.user.company_id,process_id=PDid[0], dashboard_id=PDid[1])
    data_scope_flag=str(Dashboard[4])
    rolePerm=utilb.userRolePermission(dat.user.company.id,dat.user.user_id)

    if "View Company Records" not in rolePerm and "View All Records" not in rolePerm:
        SqlQuery &= Q(company_id= '00')

    if 'View All Records' in rolePerm:
        print 'View All Records'

    elif 'View Company Records' in rolePerm:
        if len(Dashboard) >0:
            if data_scope_flag=='Y':
                for scope in ScopeData:
                    if scope['data_scope_type']=='Country':
                        SqlQuery &= Q(location_country__in= utilb.getDataScope(dat,PDid[0],'Country') )

                    if scope['data_scope_type']=='Hierarchy':
                         SqlQuery &= Q(e_employee_number__in= utilb.getDataScope(dat,PDid[0],'Hierarchy') )

            else:
                SqlQuery &= Q(e_employee_number__in= utilb.getDataScope(dat,PDid[0],'N') )


    JobStatistics = tbl.objects.values('company_id','job_id','dashboard_id').filter( SqlQuery ).annotate( total_amount=Sum('transaction_amount'),no_of_exp_reports=Count('report_id',distinct=True), no_of_exp_lines=Count('report_line_id',distinct=True), no_of_employees=Count('report_owner_id',distinct=True), avg_exp_per_report=Sum('transaction_amount')/Count('report_id',distinct=True), avg_exp_per_employee=Sum('transaction_amount')/Count('report_owner_id',distinct=True) )

    Categories = tbl.objects.values('expense_type_name').filter( SqlQuery ).annotate(category=Count('expense_type_name'),amount=Sum('transaction_amount')).order_by('expense_type_name')
    QuarterItems = tbl.objects.values('c_fiscal_quarter').filter( SqlQuery ).annotate(category=Count('c_fiscal_quarter')).order_by('c_fiscal_quarter')
    functionItems = tbl.objects.values('e_function_name').filter( SqlQuery ).annotate(category=Count('e_function_name')).order_by('e_function_name')

    Employee = tbl.objects.values('e_employee_name').filter( SqlQuery ).annotate(amount=Sum('transaction_amount'), expenses=Count('report_line_id')).order_by("e_employee_name")
    Department = tbl.objects.values('company_id', 'dashboard_id', 'e_department_name', 'location_country').filter( SqlQuery ).annotate(amount=Sum('transaction_amount'), expenses=Count('report_line_id')).order_by("e_department_name")
    GraphPaymentType = tbl.objects.values('c_month_name','payment_type_name','c_month_id').filter( SqlQuery ).annotate(amount=Sum('transaction_amount')).order_by("c_month_id")

    payment = defaultdict(list)
    for res in GraphPaymentType:
        payment[res['payment_type_name']].append([res['amount']])

    payment_month = defaultdict(list)
    for res in GraphPaymentType:
        payment_month[res['c_month_id']].append([res['amount']])

    GraphCategories = tbl.objects.values('spend_category_name').filter( SqlQuery ).annotate(amount=Sum('transaction_amount')).order_by("spend_category_name")
    GraphCountries = tbl.objects.values('location_country').filter( SqlQuery ).annotate(amount=Sum('transaction_amount')).order_by("location_country")
    BucketAnalysis = tbl.objects.values('job_id','company_id','dashboard_id','c_amount_bucket').filter( SqlQuery ).annotate(expenses=Sum('transaction_amount')).order_by("expenses")


    dat=json_data = json.dumps( {'BucketAnalysis':list(BucketAnalysis),'JobStatistics':list(JobStatistics), 'Categories_list':list(Categories),'QuarterItems':list(QuarterItems),'functionItems':list(functionItems) , 'Employee':list(Employee) , 'Department':list(Department) , 'GraphMonth':payment , 'PaymentMonth':payment_month, 'GraphCategories':list(GraphCategories) , 'GraphCountries':list(GraphCountries), 'Type':'normal' } )
    return dat




@csrf_exempt
def getDetailRecords(request):
    json_data=None
    if request.method == "POST":
        #reqdata=json.loads(request.body)
        reqdata=dict(request.POST)

        dashboardType=''.join(map(str, reqdata['dashboardType']))
        tbl=get_tbl(reqdata['dashboardType'])

        if 'countryItem' or 'QuarterItem' or 'categoryItem' or 'subCategoryItem' or 'duplicateItem' or 'functionItem' or 'employeeItem' or 'thresholdItem'  in reqdata and (reqdata['countryItem']!=[''] or reqdata['QuarterItem']!=[''] or reqdata['subCategoryItem']!=[''] or reqdata['duplicateItem']!=[''] or reqdata['categoryItem']!=[''] or reqdata['functionItem']!=[''] or reqdata['employeeItem']!=[''] or reqdata['thresholdItem']!=[''] ):
            SqlQuery=Q(company_id=request.user.company_id)

            if 'QuarterItem' in reqdata and reqdata['QuarterItem']!=['']:
                SqlQuery &= Q(c_fiscal_quarter__in=reqdata['QuarterItem'] )

            if 'countryItem' in reqdata and reqdata['countryItem']!=['']:
                SqlQuery &= Q(location_country__in=reqdata['countryItem'] )

            if 'categoryItem' in reqdata and reqdata['categoryItem']!=['']:
                SqlQuery &= Q(expense_type_name__in=reqdata['categoryItem'] )

            if 'subCategoryItem' in reqdata and reqdata['subCategoryItem']!=['']:
                SqlQuery &= Q(spend_category_name__in=reqdata['subCategoryItem'] )

            if 'duplicateItem' in reqdata and reqdata['duplicateItem']!=['']:
                duplicateItem=''.join(map(str, reqdata['duplicateItem']))
                SqlQuery &= Q(c_number_of_duplicates=duplicateItem )

            if 'functionItem' in reqdata and reqdata['functionItem']!=['']:
                SqlQuery &= Q(e_function_name__in=reqdata['functionItem'] )

            if 'employeeItem' in reqdata and reqdata['employeeItem']!=['']:
                employeeItem=''.join(map(str, reqdata['employeeItem']))
                SqlQuery &= Q(e_employee_name__icontains=employeeItem.strip())

            if 'thresholdItem' in reqdata and reqdata['thresholdItem']!=['']:
                thresholdItem=int(''.join(map(str,reqdata['thresholdItem'])))
                SqlQuery &= Q(transaction_amount__gte= thresholdItem )

            if 'start_date' and 'end_date' in reqdata and (reqdata['start_date']!=[''] and reqdata['end_date']!=['']):
                start_date=''.join(map(str, reqdata['start_date']))
                end_date=''.join(map(str, reqdata['end_date']))
                SqlQuery &= Q(transaction_date__range=[start_date,end_date] )

            if 'start_date' in reqdata and reqdata['start_date']!=[''] and reqdata['end_date']==['']:
                start_date=''.join(map(str, reqdata['start_date']))
                SqlQuery &= Q(transaction_date=start_date)


            PDid=utilb.getUserProcessDashboardId(request,dashboardType)
            Dashboard=utilb.userDashboard(request.user.company_id,request.user.user_id, PDid[0], PDid[1])
            ScopeData=AvMasterUserDatascope.objects.values('data_scope_type','company_id', 'process_id').filter(user_id=request.user.user_id, company_id=request.user.company.id , process_id = PDid[0] ).annotate( Count('company_id',distinct=True), Count('process_id',distinct=True), Count('data_scope_type',distinct=True))
            data_scope_flag=str(Dashboard[4])
            rolePerm=utilb.userRolePermission(request.user.company.id,request.user.user_id)

            if 'View All Records' in rolePerm:
                print 'View All Records'

            elif 'View Company Records' in rolePerm:
                if len(Dashboard) >0:
                    if data_scope_flag=='Y':
                        for scope in ScopeData:
                            if scope['data_scope_type']=='Country':
                                SqlQuery &= Q(location_country__in= utilb.getDataScope(request,PDid[0],'Country') )

                            if scope['data_scope_type']=='Hierarchy':
                                 SqlQuery &= Q(e_employee_number__in= utilb.getDataScope(request,PDid[0],'Hierarchy') )

                    else:
                        SqlQuery &= Q(e_employee_number__in= utilb.getDataScope(request,PDid[0],'N') )


            SqlQuery &= Q(process_id=PDid[0], dashboard_id=PDid[1])

            if 'viewBy':
                if 'viewBy' in reqdata and reqdata['viewBy']!=[]:
                    viewBy=''.join(map(str, reqdata['viewBy']))
                    if viewBy=='transaction_amount':
                        minsql=Sum('transaction_amount')
                    else:
                        minsql=Count('report_line_id')
                else:
                    minsql=Sum('transaction_amount')

            Duplicate = tbl.objects.values('e_employee_number','report_owner_id','e_employee_name','e_department_name','e_function_name','location_country','e_manager_name','report_id','report_line_id','expense_type_name','spend_category_name','payment_type_name','transaction_currency_code','transaction_amount','exchange_rate','posted_amount','approved_amount','vendor_description','location_name','description','is_personal_card_charge','receipt_received','trip_id','has_attendees','has_comments','has_exceptions').filter( SqlQuery ).order_by()

            if 'Duplicate' == dashboardType:
                export_filename=utilb.export_data(Duplicate)
            else:
                export_filename=''

            json_data = json.dumps( { 'Duplicate_list':list(Duplicate),'export_filename':export_filename } )
            utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Filter','Information','Filter',request.user.user_id,'','Expense Duplicate')

        else:
            json_data=getHighDoller(request)
    else:
        json_data=getHighDoller(request)

    return HttpResponse( json_data , content_type='application/json')




def get_tbl(typ):
    tbl=None
    dashboardType=''.join(map(str, typ))
    if 'Duplicate' == dashboardType:
        tbl = AvOutExpDashDuplicate
    elif 'High Dollar' == dashboardType:
        tbl = AvOutExpDashHighDollar
    elif 'High Mileage' == dashboardType:
        tbl = AvOutExpDashHighMileage
    elif 'Suspicious Keywords' == dashboardType:
        tbl = AvOutExpDashSuspiciousKeywords
    elif 'Excessive High Risk Expense Categories' == dashboardType:
        tbl = AvOutExpDashHighRiskExpCatg
    elif 'Personal Meals Over Threshold' == dashboardType:
        tbl = AvOutExpDashPersonalMeals
    elif 'Daily Meals Over Threshold' == dashboardType:
        tbl = AvOutExpDashDailyMeals
    elif 'High Risk Merchant Categories' == dashboardType:
        tbl = AvOutExpDashHighRiskMercCatg
    elif 'Summary Spend' == dashboardType:
        tbl = AvOutExpDashHighRiskMercCatg
    elif 'Duplicate Purchase Orders' == dashboardType:
        tbl = AvOutExpDashHighRiskMercCatg

    return tbl
