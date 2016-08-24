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
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from collections import defaultdict,OrderedDict
from django.core.signing import Signer
from django.utils.crypto import get_random_string
from django.template import Context
from django.template.loader import render_to_string, get_template
from datetime import datetime, timedelta
from django.db import connection
import utilb


@login_required(login_url='/login/')
def admin_home(request):
    current_user = request.user
    userLeftPanel = defaultdict(list)
    userDashboardACL={}
    dash=utilb.userProcessDashboard(request.user.company.id,current_user.user_id)
    for result in dash:
        userLeftPanel[result[5]].append({'dashboardName':result[6],'dashboardId':result[3]})

    datDic=dict(userLeftPanel)
    if len(datDic) >0:
        dataLeft=OrderedDict(sorted(datDic.items(), key=lambda t: t[0]))
    else:
        dataLeft=datDic

    #utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Home','Information','Home',request.user.user_id,'1','Home')
    return render_to_response('admin/index.html', {'user': current_user, 'leftPanel':dataLeft , 'rolePermission':utilb.userRolePermission(request.user.company.id,request.user.user_id),'test':'userDashboardACL'} )


@csrf_exempt
def getSearchSummary(request):
    json_data=None
    if request.method == "POST":
        #reqdata=json.loads(request.body)
        reqdata=dict(request.POST)

        if 'countryItem' or 'QuarterItem' or 'categoryItem' or 'subCategoryItem' or 'paymentItem' or 'functionItem' or 'employeeItem' or 'thresholdItem'  in reqdata and (reqdata['countryItem']!=[''] or reqdata['QuarterItem']!=[''] or reqdata['categoryItem']!=[''] or reqdata['subCategoryItem']!=[''] or reqdata['paymentItem']!=[''] or reqdata['functionItem']!=[''] or reqdata['employeeItem']!=[''] or reqdata['thresholdItem']!=[''] ):
            SqlQuery=Q(company_id=request.user.company_id)

            if 'QuarterItem' in reqdata and reqdata['QuarterItem']!=['']:
                SqlQuery &= Q(c_fiscal_quarter__in=reqdata['QuarterItem'] )

            if 'countryItem' in reqdata and reqdata['countryItem']!=['']:
                SqlQuery &= Q(location_country__in=reqdata['countryItem'] )

            if 'categoryItem' in reqdata and reqdata['categoryItem']!=['']:
                SqlQuery &= Q(expense_type_name__in=reqdata['categoryItem'] )

            if 'subCategoryItem' in reqdata and reqdata['subCategoryItem']!=['']:
                SqlQuery &= Q(spend_category_name__in=reqdata['subCategoryItem'] )

            if 'paymentItem' in reqdata and reqdata['paymentItem']!=['']:
                SqlQuery &= Q(payment_type_name__in=reqdata['paymentItem'] )

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


            PDid=utilb.getUserProcessDashboardId(request,'Summary')
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



            Employee = AvOutExpDashSummary.objects.values('e_employee_name').filter( SqlQuery ).annotate(amount=Sum('transaction_amount'), expenses=Count('report_line_id')).order_by("e_employee_name")

            Department = AvOutExpDashSummary.objects.values('company_id', 'dashboard_id', 'e_department_name', 'location_country').filter( SqlQuery ).annotate(amount=Sum('transaction_amount'), expenses=Count('report_line_id')).order_by("e_department_name")
            #GraphMonth = AvOutExpDashSummary.objects.values('c_month_name').filter( SqlQuery ).annotate(amount=minsql).order_by("c_month_id")
            GraphPaymentType = AvOutExpDashSummary.objects.values('c_month_name','payment_type_name','c_month_id').filter( SqlQuery ).annotate(amount=minsql).order_by("c_month_id")
            payment = defaultdict(list)
            for res in GraphPaymentType:
                payment[res['payment_type_name']].append([res['amount']])

            payment_month = defaultdict(list)
            for res in GraphPaymentType:
                payment_month[res['c_month_id']].append([res['amount']])

            Categories = AvOutExpDashSummary.objects.values('expense_type_name').filter( SqlQuery ).annotate(category=Count('expense_type_name'),amount=minsql).order_by('expense_type_name')
            GraphCategories = AvOutExpDashSummary.objects.values('spend_category_name').filter( SqlQuery ).annotate(amount=minsql).order_by("spend_category_name")
            GraphCountries = AvOutExpDashSummary.objects.values('location_country').filter( SqlQuery ).annotate(amount=minsql).order_by("location_country")
            SearchQuery = AvOutExpDashSummary.objects.values('company_id','job_id','dashboard_id').filter( SqlQuery ).annotate( total_amount=Sum('transaction_amount'),no_of_exp_reports=Count('report_id',distinct=True), no_of_exp_lines=Count('report_line_id',distinct=True), no_of_employees=Count('report_owner_id',distinct=True), avg_exp_per_report=Sum('transaction_amount')/Count('report_id',distinct=True), avg_exp_per_employee=Sum('transaction_amount')/Count('report_owner_id',distinct=True) )
            BucketAnalysis = AvOutExpDashSummary.objects.values('job_id','company_id','dashboard_id','c_amount_bucket').filter( SqlQuery ).filter(company_id=request.user.company_id).annotate(expenses=minsql).order_by("expenses")

            QuarterItems = AvOutExpDashSummary.objects.values('c_fiscal_quarter').filter( SqlQuery ).annotate(category=Count('c_fiscal_quarter')).order_by('c_fiscal_quarter')
            functionItems = AvOutExpDashSummary.objects.values('e_function_name').filter( SqlQuery ).annotate(category=Count('e_function_name')).order_by('e_function_name')
            json_data = json.dumps( { 'BucketAnalysis':list(BucketAnalysis),'Employee':list(Employee), 'Department':list(Department) , 'GraphMonth':payment , 'PaymentMonth':payment_month, 'GraphCategories':list(GraphCategories) ,'Categories_list':list(Categories), 'GraphCountries':list(GraphCountries) ,'JobStatistics':list(SearchQuery) ,'QuarterItems':list(QuarterItems),'functionItems':list(functionItems), 'DataType':'search'} )

            utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','Filter','Information','Filter',request.user.user_id,'','Expense Summary')

        else:
            json_data=getSummary(request)
    else:
        json_data=getSummary(request)

    return HttpResponse( json_data , content_type='application/json')



def getSummary(dat):
    PDid=utilb.getUserProcessDashboardId(dat,'Summary')
    Dashboard=utilb.userDashboard(dat.user.company_id,dat.user.user_id, PDid[0], PDid[1])
    ScopeData=AvMasterUserDatascope.objects.values('data_scope_type','company_id', 'process_id').filter(user_id=dat.user.user_id, company_id=dat.user.company.id , process_id = PDid[0] ).annotate( Count('company_id',distinct=True), Count('process_id',distinct=True), Count('data_scope_type',distinct=True))
    rolePerm=utilb.userRolePermission(dat.user.company.id,dat.user.user_id)

    SqlQuery=Q(company_id=dat.user.company_id,process_id=PDid[0], dashboard_id=PDid[1])
    data_scope_flag=str(Dashboard[4])


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



    JobStatistics = AvOutExpDashSummary.objects.values('company_id','job_id','dashboard_id').filter( SqlQuery ).annotate( total_amount=Sum('transaction_amount'),no_of_exp_reports=Count('report_id',distinct=True), no_of_exp_lines=Count('report_line_id',distinct=True), no_of_employees=Count('report_owner_id',distinct=True), avg_exp_per_report=Sum('transaction_amount')/Count('report_id',distinct=True), avg_exp_per_employee=Sum('transaction_amount')/Count('report_owner_id',distinct=True) )
    Categories = AvOutExpDashSummary.objects.values('expense_type_name').filter( SqlQuery ).annotate(category=Count('expense_type_name'),amount=Sum('transaction_amount')).order_by('expense_type_name')
    QuarterItems = AvOutExpDashSummary.objects.values('c_fiscal_quarter').filter( SqlQuery ).annotate(category=Count('c_fiscal_quarter')).order_by('c_fiscal_quarter')
    functionItems = AvOutExpDashSummary.objects.values('e_function_name').filter( SqlQuery ).annotate(category=Count('e_function_name')).order_by('e_function_name')
    paymentType = AvOutExpDashSummary.objects.values('payment_type_name').filter( SqlQuery ).annotate(paymentType=Count('payment_type_name')).order_by('payment_type_name')

    Employee = AvOutExpDashSummary.objects.values('e_employee_name').filter( SqlQuery ).annotate(amount=Sum('transaction_amount'), expenses=Count('report_line_id')).order_by("e_employee_name")
    Department = AvOutExpDashSummary.objects.values('company_id', 'dashboard_id', 'e_department_name', 'location_country').filter( SqlQuery ).annotate(amount=Sum('transaction_amount'), expenses=Count('report_line_id')).order_by("e_department_name")
    #GraphMonth = AvOutExpDashSummary.objects.values('c_month_name').filter( SqlQuery ).annotate(amount=Sum('transaction_amount')).order_by("c_month_id")
    GraphPaymentType = AvOutExpDashSummary.objects.values('c_month_name','payment_type_name','c_month_id').filter( SqlQuery ).annotate(amount=Sum('transaction_amount')).order_by("c_month_id")

    payment = defaultdict(list)
    for res in GraphPaymentType:
        payment[res['payment_type_name']].append([res['amount']])

    payment_month = defaultdict(list)
    for res in GraphPaymentType:
        payment_month[res['c_month_id']].append([res['amount']])

    GraphCategories = AvOutExpDashSummary.objects.values('spend_category_name').filter( SqlQuery ).annotate(amount=Sum('transaction_amount')).order_by("spend_category_name")
    GraphCountries = AvOutExpDashSummary.objects.values('location_country').filter( SqlQuery ).annotate(amount=Sum('transaction_amount')).order_by("location_country")
    BucketAnalysis=AvOutExpDashSummary.objects.values('job_id','company_id','dashboard_id','c_amount_bucket').filter( SqlQuery ).annotate(expenses=Sum('transaction_amount')).order_by("expenses")

    # sql_string = 'SELECT company_id, dashboard_id, amount_bucket, expenses FROM av_engine.av_out_exp_buckets_summary_v WHERE company_id=%s order by expenses DESC' %dat.user.company_id
    # cursor.execute(sql_string)
    # result = cursor.fetchall()

    dat=json_data = json.dumps( {'BucketAnalysis':list(BucketAnalysis),'JobStatistics':list(JobStatistics), 'Categories_list':list(Categories),'QuarterItems':list(QuarterItems),'functionItems':list(functionItems) , 'paymentType':list(paymentType) , 'Employee':list(Employee) , 'Department':list(Department) , 'GraphMonth':payment , 'PaymentMonth':payment_month, 'GraphCategories':list(GraphCategories) , 'GraphCountries':list(GraphCountries) ,'Type':'normal' } )
    return dat



def login(request):
    log_message= None
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        cmp = request.POST.get('companyname').strip()
        cmpData = AvMasterCompany.objects.filter(short_name=cmp)
        if len(cmpData)>0:
            cmpid=cmpData[0].id
        else:
            cmpid=0;
        user = authenticate(user_id = username , password = password)
        if user:
            if user.company_id==cmpid:
                auth_login(request, user)
                utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','User Login','Information','User Login',request.user.user_id,'','User Login')
                return HttpResponseRedirect('/')
            else:
                log_message = 'Wrong company name'
                utilb.logManage(1,cmp,datetime.now(),'User Activity','Incorrect Company Name','Information','Incorrect Company Name',username,'','Incorrect Company Name')
        else:
            log_message = 'Wrong username or password'
            utilb.logManage(1,cmp,datetime.now(),'User Activity','Incorrect Username','Information','Incorrect Username',username,'','Incorrect Username Password')
    context={
            'log_message': log_message
    }
    return render(request,'admin/login.html',context)



def forgotUserName(request):
    log_message= None
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        email_address = request.POST.get('email_address')
        cmp = request.POST.get('companyname').strip()
        parm = [email_address,cmp]
        cursor = connection.cursor()
        cursor.execute('SELECT u.*,c.short_name FROM av_master_company_users u LEFT JOIN av_master_company c ON u.company_id=c.id WHERE u.email_address = %s AND c.short_name = %s ', parm)
        result=cursor.fetchone()
        cursor.close()
        if result!=None:
            from_email = 'noreply@audvantage.com'
            msg = """<p><strong style="color:#565252;">Dear </strong> %s,</p>
            <p>We got the word that you forgot your Username. No problem, these things happen.</p>
            <p>If this was a mistake, just ignore this email and nothing will happen.</p>
            <p><br/><strong style="color:#565252;">Your Username is:</strong> %s</p>
            <p><br/><br/><br/><strong>Best,</strong> <br/> Audvantage Team</p>
            """ %(result[4],result[1])

            ctx = { 'body': msg }
            message = get_template('admin/email-template/email.html').render(Context(ctx))
            msg = EmailMessage('Audvantage::Forgot UserName', message, to=[result[7]], from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            log_message = '<div class="alert alert-success" role="alert">We have sent mail on your email Address, Please check your mail</div>'
            utilb.logManage(1,cmp,datetime.now(),'User Activity','Forgot Username','Information','Forgot Username',result[1],'','Forgot Username')
        else:
            log_message = '<div class="alert alert-danger" role="alert">Wrong Company Name or Email Address </div>'

    context={
            'log_message': log_message
    }
    return render(request,'admin/forgot-username.html',context)



def forgotPassword(request):
    log_message= None
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        cmp = request.POST.get('companyname').strip()
        parm = [username,cmp]
        cursor = connection.cursor()
        cursor.execute('SELECT u.*,c.short_name FROM av_master_company_users u LEFT JOIN av_master_company c ON u.company_id=c.id WHERE u.user_id = %s AND c.short_name = %s ', parm)
        result=cursor.fetchone()
        cursor.close()

        if result!=None:
            signer = Signer()
            value = signer.sign(result[0])
            v=value.split(':')
            unique_id=get_random_string(length=16)
            unqvalue = v[-1]+unique_id
            AvMasterCompanyUsers.objects.filter(id=result[0]).update(token_id=unqvalue, token_date=datetime.now())

            from_email = 'noreply@audvantage.com'
            msg = """<p><strong style="color:#565252;">Dear </strong> %s,</p>
            <p>We got the word that you forgot your Password. No problem, these things happen.</p>
            <p>If this was a mistake, just ignore this email and nothing will happen.</p>
            <p><br/> Please click on the below link for reset your password <br/><a href="%s">/%s</a></p>
            <p><br/><br/><br/><strong>Best,</strong> <br/> Audvantage Team</p>
            """ %(result[4],'http://'+request.META['HTTP_HOST']+'/reset-password/'+unqvalue, unqvalue)

            ctx = { 'body': msg }
            message = get_template('admin/email-template/email.html').render(Context(ctx))
            msg = EmailMessage('Audvantage::Forgot Password', message, to=[result[7]], from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            log_message = '<div class="alert alert-success" role="alert">We have sent a link on your email Address, Please check your mail</div>'
            utilb.logManage(1,cmp,datetime.now(),'User Activity','Forgot Password','Information','Forgot Password',result[7],'','Forgot Password')
        else:
            log_message = '<div class="alert alert-danger" role="alert">Wrong Company Name or UserName </div>'

    context={
            'log_message': log_message
    }
    return render(request,'admin/forgot-password.html',context)


def resetPassword(request,id):
    log_message= ''
    if request.user.is_authenticated():
       return HttpResponseRedirect('/')

    user=AvMasterCompanyUsers.objects.filter(token_id=id)
    if len(user)==0:
        return HttpResponseRedirect('/forgot-password/')

    a=user[0].token_date
    b=datetime.now()
    c=b-a
    dd=divmod(c.days * 86400 + c.seconds, 60)

    if dd[0]>20:
        return HttpResponseRedirect('/forgot-password/')

    if request.method == "POST":
            if request.POST.get('new_password')==request.POST.get('re_password'):
                u = AvMasterCompanyUsers.objects.get(id=user[0].id)
                u.set_password(request.POST.get('new_password'))
                u.save()
                log_message='success'
                from_email = 'noreply@audvantage.com'
                msg = """<p><strong style="color:#565252;">Dear </strong> %s,</p>
                <p>Your password has been successfully updated.<br/> Please see the below login details</p>
                <p><strong style="color:#565252;">Username:</strong> %s</p>
                <p><strong style="color:#565252;">Password:</strong> %s</p>
                <p><br/><br/><br/><strong>Best,</strong> <br/> Audvantage Team</p>
                """ %(user[0].first_name,user[0].user_id,request.POST.get('new_password'))

                ctx = { 'body': msg }
                message = get_template('admin/email-template/email.html').render(Context(ctx))
                msg = EmailMessage('Audvantage::Password reset confirmation', message, to=[user[0].email_address], from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()
            else:
                log_message = '<div class="alert alert-danger" role="alert">New Password and Confirm Password do not match </div>'

    context={
        'log_message': log_message,'Userinfo':user[0]
    }
    return render(request,'admin/reset-password.html',context)


def logout_page(request):
    utilb.logManage(request.user.company.id,request.user.company.short_name,datetime.now(),'User Activity','User Logout','Information','User Logout',request.user.user_id,'','User Logout')
    logout(request)
    return HttpResponseRedirect('/login/')
