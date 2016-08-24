# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AvOutExpDashSummary(models.Model):
    id = models.BigIntegerField(primary_key=True)
    job_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    dashboard_id = models.BigIntegerField()
    report_id = models.CharField(max_length=200)
    report_line_id = models.CharField(max_length=200)
    report_owner_id = models.CharField(max_length=200)
    expense_type_name = models.CharField(max_length=240)
    location_country = models.CharField(max_length=240)
    spend_category_name = models.CharField(max_length=240)
    e_employee_name = models.CharField(max_length=240)
    e_function_name = models.CharField(max_length=240)
    c_fiscal_quarter = models.CharField(max_length=240)
    transaction_amount = models.BigIntegerField()
    report_line_id = models.CharField(max_length=240)
    c_month_name = models.CharField(max_length=240)
    e_department_name = models.CharField(max_length=240)
    e_employee_number = models.BigIntegerField()
    e_manager_employee_number = models.CharField(max_length=240)
    payment_type_name = models.CharField(max_length=240)
    transaction_date = models.DateField()
    transaction_currency_code = models.CharField(max_length=240)
    exchange_rate = models.BigIntegerField()
    posted_amount = models.BigIntegerField()
    approved_amount = models.BigIntegerField()
    vendor_description = models.CharField(max_length=240)
    location_name = models.CharField(max_length=240)
    description = models.CharField(max_length=240)
    is_personal_card_charge = models.CharField(max_length=240)
    receipt_received = models.CharField(max_length=240)
    trip_id = models.CharField(max_length=240)
    has_attendees = models.CharField(max_length=240)
    has_comments = models.CharField(max_length=240)
    has_exceptions = models.CharField(max_length=240)
    c_amount_bucket = models.CharField(max_length=240)
    c_month_id = models.CharField(max_length=240)

    class Meta:
        managed = False
        db_table = 'av_out_exp_dash_summary'


class AvExpJobStatistics(models.Model):
    id = models.BigIntegerField(primary_key=True)
    job_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    no_of_exp_reports = models.BigIntegerField(blank=True, null=True)
    no_of_exp_lines = models.BigIntegerField(blank=True, null=True)
    avg_exp_per_report = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    avg_exp_per_employee = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    no_of_employees = models.BigIntegerField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'av_exp_job_statistics'
        unique_together = (('job_id', 'check_id', 'company_id'),)


class AvOutExpExpensesF(models.Model):
    id = models.BigIntegerField(primary_key=True)
    job_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    dashboard_id = models.BigIntegerField()
    report_id = models.CharField(max_length=200)
    report_line_id = models.CharField(max_length=200)
    report_owner_id = models.CharField(max_length=200)
    expense_type_name = models.CharField(max_length=240)
    location_country = models.CharField(max_length=240)
    spend_category_name = models.CharField(max_length=240)
    e_employee_name = models.CharField(max_length=240)
    e_function_name = models.CharField(max_length=240)
    c_fiscal_quarter = models.CharField(max_length=240)
    transaction_amount = models.BigIntegerField()
    report_line_id = models.CharField(max_length=240)
    c_month_name = models.CharField(max_length=240)
    e_department_name = models.CharField(max_length=240)
    e_employee_number = models.BigIntegerField()
    e_manager_employee_number = models.CharField(max_length=240)
    payment_type_name = models.CharField(max_length=240)
    transaction_date = models.DateField()
    transaction_currency_code = models.CharField(max_length=240)
    exchange_rate = models.BigIntegerField()
    posted_amount = models.BigIntegerField()
    approved_amount = models.BigIntegerField()
    vendor_description = models.CharField(max_length=240)
    location_name = models.CharField(max_length=240)
    description = models.CharField(max_length=240)
    is_personal_card_charge = models.CharField(max_length=240)
    receipt_received = models.CharField(max_length=240)
    trip_id = models.CharField(max_length=240)
    has_attendees = models.CharField(max_length=240)
    has_comments = models.CharField(max_length=240)
    has_exceptions = models.CharField(max_length=240)

    class Meta:
        managed = False
        db_table = 'av_out_exp_expenses_f'


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


class AvMasterCompanyMessage(models.Model):
    id = models.BigIntegerField(primary_key=True)
    company = models.ForeignKey(AvMasterCompany, models.DO_NOTHING, blank=True, null=True)
    message_type = models.CharField(max_length=1)
    message_text = models.CharField(max_length=400)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_company_message'


class AvMasterCompanyProcess(models.Model):
    id = models.BigIntegerField(primary_key=True)
    company = models.ForeignKey(AvMasterCompany, models.DO_NOTHING, blank=True, null=True)
    process = models.ForeignKey('AvMasterProcess', models.DO_NOTHING, blank=True, null=True)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_company_process'


from django.contrib.auth.models import UserManager
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class AvMasterCompanyUsers(AbstractBaseUser):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.CharField(max_length=30, unique=True)
    # company_id = models.BigIntegerField()
    company = models.ForeignKey(AvMasterCompany, models.DO_NOTHING, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    nick_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email_address = models.CharField(max_length=200, blank=True, null=True)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)
    token_id = models.CharField(max_length=100)
    token_date = models.DateTimeField()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'av_master_company_users'



class AvMasterDashboard(models.Model):
    id = models.BigIntegerField(primary_key=True)
    short_name = models.CharField(max_length=40)
    long_name = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    dashboard_image = models.BinaryField()
    version = models.CharField(max_length=20)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_dashboard'


class AvMasterFunctions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    function_name = models.CharField(max_length=240)
    description = models.CharField(max_length=400, blank=True, null=True)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_functions'


class AvMasterProcess(models.Model):
    id = models.BigIntegerField(primary_key=True)
    short_name = models.CharField(max_length=40)
    long_name = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    process_image = models.BinaryField()
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_process'


class AvMasterProcessDashboards(models.Model):
    id = models.BigIntegerField(primary_key=True)
    process = models.ForeignKey(AvMasterProcess, models.DO_NOTHING, blank=True, null=True)
    dashboard = models.ForeignKey(AvMasterDashboard, models.DO_NOTHING, blank=True, null=True)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_process_dashboards'


class AvMasterRoleFunctions(models.Model):
    role = models.ForeignKey('AvMasterRoles', models.DO_NOTHING)
    function = models.ForeignKey(AvMasterFunctions, models.DO_NOTHING)
    comments = models.CharField(max_length=400, blank=True, null=True)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_role_functions'


class AvMasterRoles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    role_name = models.CharField(max_length=240)
    description = models.CharField(max_length=400, blank=True, null=True)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_roles'


class AvMasterUserDashboard(models.Model):
    id = models.BigIntegerField(primary_key=True)
    company = models.ForeignKey(AvMasterCompany, models.DO_NOTHING, blank=True, null=True)
    user_id = models.CharField(max_length=30)
    process = models.ForeignKey(AvMasterProcess, models.DO_NOTHING, blank=True, null=True)
    dashboard = models.ForeignKey(AvMasterDashboard, models.DO_NOTHING, blank=True, null=True)
    data_scope_flag = models.CharField(max_length=1)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_user_dashboard'


class AvMasterUserDatascope(models.Model):
    process_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    user_id = models.CharField(max_length=30)
    data_scope_type = models.CharField(max_length=100)
    data_scope_value = models.CharField(max_length=100)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_user_datascope'


class AvMasterUserRoles(models.Model):
    company_id = models.BigIntegerField()
    user_id = models.CharField(max_length=30)
    role_id = models.BigIntegerField()
    comments = models.CharField(max_length=400, blank=True, null=True)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_master_user_roles'


class AvSetupDashExpCountries(models.Model):
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    country = models.CharField(max_length=200)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_setup_dash_exp_countries'


class AvSetupDashExpEmployees(models.Model):
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    employee_id = models.CharField(max_length=200)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_setup_dash_exp_employees'


class AvSetupDashExpKeywords(models.Model):
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    keyword = models.CharField(max_length=200)
    match_condition = models.CharField(max_length=10)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_setup_dash_exp_keywords'


class AvSetupDashExpMccCodes(models.Model):
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    mcc_code_id = models.BigIntegerField()
    mcc_code_description = models.CharField(max_length=200)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_setup_dash_exp_mcc_codes'


class AvSetupDashExpSettings(models.Model):
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    comments = models.CharField(max_length=400, blank=True, null=True)
    expense_type = models.CharField(max_length=1)
    spend_category = models.CharField(max_length=1)
    keywords = models.CharField(max_length=1)
    mcc_codes = models.CharField(max_length=1)
    countries = models.CharField(max_length=1)
    employees = models.CharField(max_length=1)
    amount_threshold = models.BigIntegerField()
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)
    run_check = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'av_setup_dash_exp_settings'


class AvSetupDashExpSpends(models.Model):
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    spend_category = models.CharField(max_length=200)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_setup_dash_exp_spends'


class AvSetupDashExpTypes(models.Model):
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    expense_type = models.CharField(max_length=200)
    active_flag = models.CharField(max_length=1)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_setup_dash_exp_types'


class AvSsDashExpCountries(models.Model):
    job_id = models.BigIntegerField()
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    country = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_ss_dash_exp_countries'


class AvSsDashExpEmployees(models.Model):
    job_id = models.BigIntegerField()
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    employee_id = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_ss_dash_exp_employees'


class AvSsDashExpKeywords(models.Model):
    job_id = models.BigIntegerField()
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    keyword = models.CharField(max_length=200)
    match_condition = models.CharField(max_length=10)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_ss_dash_exp_keywords'


class AvSsDashExpMccCodes(models.Model):
    job_id = models.BigIntegerField()
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    mcc_code_id = models.BigIntegerField()
    mcc_code_description = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_ss_dash_exp_mcc_codes'


class AvSsDashExpSettings(models.Model):
    job_id = models.BigIntegerField()
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    comments = models.CharField(max_length=400, blank=True, null=True)
    expense_type = models.CharField(max_length=1)
    spend_category = models.CharField(max_length=1)
    keywords = models.CharField(max_length=1)
    mcc_codes = models.CharField(max_length=1)
    countries = models.CharField(max_length=1)
    employees = models.CharField(max_length=1)
    amount_threshold = models.BigIntegerField()
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_ss_dash_exp_settings'


class AvSsDashExpSpends(models.Model):
    job_id = models.BigIntegerField()
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    spend_category = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_ss_dash_exp_spends'


class AvSsDashExpTypes(models.Model):
    job_id = models.BigIntegerField()
    setting_id = models.BigIntegerField()
    process_id = models.BigIntegerField()
    check_id = models.BigIntegerField()
    company_id = models.BigIntegerField()
    expense_type = models.CharField(max_length=200)
    last_updated_date = models.DateTimeField()
    last_updated_by = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'av_ss_dash_exp_types'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.CharField(max_length=400)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
