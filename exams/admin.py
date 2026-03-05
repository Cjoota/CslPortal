from django.contrib import admin
from exams.models import Exam

class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'patient', 'company', 'collected_date', 'exam_status', 'exam_status_date', 'created_at')
    search_fields = ('name', 'patient', 'company', 'collected_date', 'exam_status', 'exam_status_date')
admin.site.register(Exam, ExamAdmin)