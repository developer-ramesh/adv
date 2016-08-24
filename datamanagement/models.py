from __future__ import unicode_literals

from django.db import models

class AvMasterUploadDataType(models.Model):
    id = models.BigIntegerField(primary_key=True)
    data_type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'av_master_upload_data_type'



class AvTrxnCompanyEmployeesS(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    data_upload_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    employee_id = models.CharField(max_length=30)
    employee_number = models.BigIntegerField()
    employee_email = models.CharField(max_length=240)
    first_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assignment_status = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    department_code = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    function_name = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    manager_employee_number = models.BigIntegerField()
    active_flag = models.CharField(max_length=2)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)
    record_insert_date = models.DateTimeField()
    record_insert_by = models.CharField(max_length=200)
    custom_field1 = models.CharField(max_length=200)
    custom_field2 = models.CharField(max_length=200)
    custom_field3 = models.CharField(max_length=200)
    custom_field4 = models.CharField(max_length=200)
    custom_field5 = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'av_trxn_company_employees_s'


class AvTrxnExpExpensesS(models.Model):
    data_upload_id = models.BigIntegerField()
    source_system = models.CharField(max_length=200)
    company_id = models.BigIntegerField()
    report_id = models.CharField(max_length=200)
    report_line_id = models.CharField(max_length=200)
    report_owner_id = models.CharField(max_length=200)
    expense_type_code = models.CharField(max_length=100)
    expense_type_name = models.CharField(max_length=240)
    spend_category_code = models.CharField(max_length=100)
    spend_category_name = models.CharField(max_length=240)
    payment_type_id = models.CharField(max_length=100)
    payment_type_name = models.CharField(max_length=240)
    transaction_date = models.DateTimeField()
    transaction_currency_code = models.CharField(max_length=100)
    transaction_amount = models.BigIntegerField()
    exchange_rate = models.BigIntegerField()
    posted_amount = models.BigIntegerField()
    approved_amount = models.BigIntegerField()
    vendor_description = models.CharField(max_length=240)
    vendor_list_item_id = models.CharField(max_length=100)
    vendor_list_item_name = models.CharField(max_length=240)
    location_id = models.CharField(max_length=100)
    location_name = models.CharField(max_length=240)
    location_subdivision = models.CharField(max_length=240)
    location_country = models.CharField(max_length=240)
    description = models.CharField(max_length=240)
    is_personal = models.CharField(max_length=100)
    is_billable = models.CharField(max_length=100)
    is_personal_card_charge = models.CharField(max_length=100)
    has_image = models.CharField(max_length=100)
    is_image_required = models.CharField(max_length=100)
    receipt_received = models.CharField(max_length=100)
    tax_receipt_type = models.CharField(max_length=100)
    electronic_receipt_id = models.CharField(max_length=200)
    company_card_transaction_id = models.CharField(max_length=200)
    trip_id = models.CharField(max_length=200)
    has_itemizations = models.CharField(max_length=100)
    allocation_type = models.CharField(max_length=100)
    has_attendees = models.CharField(max_length=100)
    has_vat = models.CharField(max_length=100)
    has_applied_cash_advance = models.CharField(max_length=100)
    has_comments = models.CharField(max_length=100)
    has_exceptions = models.CharField(max_length=100)
    is_paid_by_expense_pay = models.CharField(max_length=100)
    employee_bank_account_id = models.CharField(max_length=200)
    journey = models.CharField(max_length=200)
    last_modified = models.DateTimeField()
    last_modified_by = models.CharField(max_length=200)
    org_unit = models.CharField(max_length=200)
    record_insert_date = models.DateTimeField()
    record_insert_by = models.CharField(max_length=200)
    custom_field1 = models.CharField(max_length=200)
    custom_field2 = models.CharField(max_length=200)
    custom_field3 = models.CharField(max_length=200)
    custom_field4 = models.CharField(max_length=200)
    custom_field5 = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'av_trxn_exp_expenses_s'


class AvLogDataUploads(models.Model):
    data_upload_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    company_name = models.CharField(max_length=40)
    data_type = models.CharField(max_length=100)
    uploaded_by = models.CharField(max_length=200)
    uploaded_date = models.DateTimeField()
    no_of_records = models.CharField(max_length=200)
    status = models.CharField(max_length=800)
    upload_or_rollback = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'av_log_data_uploads'


class AvLogAuditTrail(models.Model):
    company_id = models.BigIntegerField()
    company_name = models.CharField(max_length=40)
    event_date = models.DateTimeField()
    event_category = models.CharField(max_length=240)
    event_sub_category = models.CharField(max_length=240)
    event_type = models.CharField(max_length=240)
    description = models.CharField(max_length=4000)
    event_user = models.CharField(max_length=30)
    object_id = models.CharField(max_length=400)
    object_name = models.CharField(max_length=400)

    class Meta:
        managed = False
        db_table = 'av_log_audit_trail'


class AvMasterCompany(models.Model):
    id = models.BigIntegerField(primary_key=True)
    short_name = models.CharField(max_length=40)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.BigIntegerField(blank=True, null=True)
    logo = models.BinaryField(blank=True, null=True)
    primary_contact_name = models.CharField(max_length=150)
    primary_contact_email = models.CharField(max_length=150)
    primary_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    secondary_contact_name = models.CharField(max_length=150, blank=True, null=True)
    secondary_contact_email = models.CharField(max_length=150, blank=True, null=True)
    secondary_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    landing_page_text = models.BinaryField(blank=True, null=True)
    single_sign_on_flag = models.CharField(max_length=1)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_company'


class AvMasterEvents(models.Model):
    id = models.BigIntegerField(primary_key=True)
    event_type = models.CharField(max_length=240)
    event_category = models.CharField(max_length=240, blank=True, null=True)
    event_sub_category = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'av_master_events'
