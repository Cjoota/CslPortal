from django.contrib import admin
from patients.models import Patient
# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company','exam_type', 'exam_path', 'created_at')
    search_fields = ('name', 'company',)
    
admin.site.register(Patient, PatientAdmin)