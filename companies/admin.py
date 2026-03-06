from django.contrib import admin
from companies.models import Company, SubCompany

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cnpj', 'address', 'phone', 'email', 'sub_company', 'created_at')
    search_fields = ('name', 'cnpj', 'address', 'phone', 'email')
    list_filter = ('created_at',)
    list_per_page = 10
    list_max_show_all = 100

class SubCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cnpj', 'created_at')
    search_fields = ('name', 'cnpj')
    list_filter = ('created_at',)
    list_per_page = 10
    list_max_show_all = 100
    
admin.site.register(Company, CompanyAdmin)

admin.site.register(SubCompany, SubCompanyAdmin)