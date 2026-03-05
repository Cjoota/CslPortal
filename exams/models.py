from django.db import models
from companies.models import Company
from patients.models import Patient

class ExamStatus(models.TextChoices):
    PENDENTE = 'pendente'
    COLETADO = 'coletado'
    AGUARDANDO_RESULTADOS = 'aguardando_resultados'
    PRONTO = 'pronto'

class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=False, blank=False, related_name='exams_patient')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, blank=False, related_name='exams_company')
    collected_date = models.DateField(null=True, blank=True)
    exam_status = models.CharField(max_length=255, null=False, blank=False, choices=ExamStatus.choices)
    exam_status_date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
    def __str__(self):
        return self.name
    

    
    