from django.db import connection
import datetime , time
import xlwt



def userRolePermission(compId,usrId):
    parm=[compId,usrId]
    cursor = connection.cursor()
    cursor.execute("SELECT u.company_id, u.user_id, p.permission FROM av_master_user_roles u, av_master_role_permissions rp, av_master_permissions p WHERE u.role_id = rp.role_id AND rp.permission_id = p.id AND u.company_id = %s AND u.user_id = %s ORDER BY p.id",parm)
    result = cursor.fetchall()
    arr=[]
    for row in result:
        arr.append(row[2])
    cursor.close()
    return arr

def logManage(compId,comName,dat,cat,sub_cat,typ,des,usId,obId,obName):
    cursor = connection.cursor()
    sqlqry="INSERT INTO av_log_audit_trail(company_id, company_name, event_date, event_category, event_sub_category, event_type, description, event_user, object_id, object_name)VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(compId,comName,dat,cat,sub_cat,typ,des,usId,obId,obName)
    cursor.execute(sqlqry)
    #result=cursor.fetchone()
    cursor.close()
    print compId


def export_auditlog(data):
    file_name = 'static/tmp/Audit-Log-'+str(int(round(time.time() * 1000)))+'.xls'
    todo_obj=data
    #response = HttpResponse(content_type='application/ms-excel')
    #response['Content-Disposition'] = 'attachment; filename=%s' %(file_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Todo")

    row_num = 0
    columns = [ (u"Company Name", 4000), (u"Event Date", 8000), (u"Event Category", 8000), (u"Event Sub Category", 8000), (u"Event Type", 8000) ,(u"User Name", 8000), (u"Event Description", 8000),]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in todo_obj:
        row_num += 1
        row = [
            obj.company_name,
            obj.event_date.strftime("%Y-%m-%d %H:%M"),
            obj.event_category,
            obj.event_sub_category,
            obj.event_type,
            obj.event_user,
            obj.description,
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    fl=wb.save(file_name)
    return file_name


def export_data(data):
    file_name = 'static/tmp/'+str(int(round(time.time() * 1000)))+'.xls'
    todo_obj=data
    #response = HttpResponse(content_type='application/ms-excel')
    #response['Content-Disposition'] = 'attachment; filename=%s' %(file_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Todo")

    row_num = 0
    columns = [ (u"Employee Number", 6000), (u"Employee Email", 8000), (u"Employee Name", 8000), (u"Department Name", 8000), (u"Function", 8000) ,(u"Country", 8000), (u"Manager Name", 8000),(u"Report ID", 8000),(u"Report Line ID", 8000),(u"Expense Type Name", 8000),(u"Spend Category Name", 8000),(u"Payment Type Name", 8000),(u"Transaction Currency Code", 8000),(u"Transaction Amount", 8000),(u"Exchange Rate", 8000),(u"Posted Amount", 8000),(u"Approved Amount", 8000),(u"Vendor Description", 8000),(u"Location Name", 8000),(u"Description", 8000),(u"Is Personal Card Charge", 8000),(u"Receipt Received", 8000),(u"Trip ID", 8000),(u"Has Attendees", 8000),(u"Has Comments", 8000),(u"Has Exceptions", 8000),(u"# Duplicates", 8000),(u"Total Duplicate Amount", 8000),]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in todo_obj:
        row_num += 1
        row = [
            obj['e_employee_number'],
            obj['report_owner_id'],
            obj['e_employee_name'],
            obj['e_department_name'],
            obj['e_function_name'],
            obj['location_country'],
            obj['e_manager_name'],
            obj['report_id'],
            obj['report_line_id'],
            obj['expense_type_name'],
            obj['spend_category_name'],
            obj['payment_type_name'],
            obj['transaction_currency_code'],
            obj['transaction_amount'],
            obj['exchange_rate'],
            obj['posted_amount'],
            obj['approved_amount'],
            obj['vendor_description'],
            obj['location_name'],
            obj['description'],
            obj['is_personal_card_charge'],
            obj['receipt_received'],
            obj['trip_id'],
            obj['has_attendees'],
            obj['has_comments'],
            obj['has_exceptions'],
            #obj['c_number_of_duplicates'],
            #obj['c_total_duplicate_amount'],
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    fl=wb.save(file_name)
    return file_name



def userProcessDashboard(compId,usrId):
    parm=[compId,usrId,usrId]
    cursor = connection.cursor()
    cursor.execute("SELECT upd.user_id, cpd.company_id, cpd.process_id, upd.dashboard_id, up.data_scope_flag,mp.short_name,md.short_name FROM av_master_company_process_dashboards cpd, av_master_user_process_dashboards upd, av_master_user_process up, av_master_process mp, av_master_dashboard md WHERE cpd.company_id = upd.company_id AND cpd.process_id = upd.process_id AND cpd.dashboard_id = upd.dashboard_id AND upd.process_id = up.process_id AND mp.id=upd.process_id AND md.id=upd.dashboard_id AND cpd.company_id = %s AND upd.user_id = %s AND up.user_id = %s",parm)
    result = cursor.fetchall()
    cursor.close()
    return result


def userDashboard(compId,usrId,pId,dId):
    parm=[compId,usrId,usrId,pId,dId]
    cursor = connection.cursor()
    cursor.execute("SELECT upd.user_id, cpd.company_id, cpd.process_id, upd.dashboard_id, up.data_scope_flag,mp.short_name,md.short_name FROM av_master_company_process_dashboards cpd, av_master_user_process_dashboards upd, av_master_user_process up, av_master_process mp, av_master_dashboard md WHERE cpd.company_id = upd.company_id AND cpd.process_id = upd.process_id AND cpd.dashboard_id = upd.dashboard_id AND upd.process_id = up.process_id AND mp.id=upd.process_id AND md.id=upd.dashboard_id AND cpd.company_id = %s AND upd.user_id = %s AND up.user_id = %s AND cpd.process_id=%s AND upd.dashboard_id=%s",parm)
    result = cursor.fetchone()
    cursor.close()
    return result


def customQryExc(sqlQry):
    cursor = connection.cursor()
    cursor.execute(sqlQry)
    result = cursor.fetchall()
    cursor.close()
    return result


def getUserProcessDashboardId(dat,dtype):
    parm = [dat.user.user_id,dat.user.company.id,dtype]
    cursor = connection.cursor()
    cursor.execute('SELECT m.process_id,m.dashboard_id FROM av_master_user_process_dashboards m LEFT JOIN  av_master_dashboard d ON m.dashboard_id=d.id WHERE m.user_id = %s AND m.company_id = %s AND d.short_name = %s', parm)
    return cursor.fetchone()


def getDataScope(dat,process,dtype):
    cursor = connection.cursor()

    if dtype=='Country':
        parm =  [dat.user.user_id, dat.user.company_id, process]
        cursor.execute("SELECT data_scope_value FROM av_master_user_datascope WHERE user_id = %s AND company_id = %s AND process_id = %s AND data_scope_type = 'Country'", parm)
        result = cursor.fetchall()
        cursor.close()
        arr=[]
        for scope in result:
            arr.append(scope[0])
        return arr;

    elif dtype=='N':
        parm =  [dat.user.company_id,dat.user.user_id, dat.user.company_id]
        cursor.execute("SELECT employee_number FROM av_engine.av_trxn_company_employee_proxy_vw WHERE company_id = %s AND proxy_employee_number IN (SELECT CAST(employee_number AS bigint) FROM av_master_company_users WHERE user_id = %s AND company_id = %s)", parm)
        result = cursor.fetchall()
        cursor.close()
        arr=[]
        for scope in result:
            arr.append(scope[0])
        return arr;

    else:
        parm =  [dat.user.company_id, dat.user.user_id, dat.user.company_id, process]
        cursor.execute("SELECT employee_number FROM av_engine.av_trxn_company_employee_proxy_vw WHERE company_id = %s AND proxy_employee_number IN (SELECT CAST(data_scope_value AS bigint) FROM av_master_user_datascope WHERE user_id = %s AND company_id = %s AND process_id = %s AND data_scope_type = 'Hierarchy')", parm)
        result = cursor.fetchall()
        cursor.close()
        arr=[]
        for empNo in result:
            arr.append(int(empNo[0]))
        return arr
