from django.contrib import admin
from referrals.models import Referrals
# Register your models here.
class ReferralsAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_name', 'employee_cpf', 'employee_birth_date', 'employee_function', 'employee_sector', 'company_name', 'exam_type', 'adm_date', 'done', 'created_at')
    search_fields = ('employee_name', 'employee_cpf', 'employee_birth_date', 'employee_function', 'employee_sector', 'company_name', 'exam_type', 'adm_date', 'done', 'created_at')
    
admin.site.register(Referrals, ReferralsAdmin)