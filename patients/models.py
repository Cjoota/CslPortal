import datetime
from django.db import models
from companies.models import Company


# Create your models here.
# class ExamType(models.TextChoices):
#     ADMISSIONAL = 'admissional'
#     DEMISIONAL = 'demisional'
#     PERIODICO = 'periodico'
#     RETORNO_A_FUNÇÃO = 'retorno_a_funcao'
#     MUDANÇA_DE_RISCOS = 'mudanca_de_risco'

def user_directory_path(instance, filename):
    # O arquivo será salvo em MEDIA_ROOT/exames/empresa_<id>/<filename>
    return f'exames/company_{instance.company.id}/{filename}'

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, blank=False, related_name='patients_company')
    exam_type = models.CharField(max_length=255, null=False, blank=False, default='admissional')
    exam_path = models.FileField(upload_to=user_directory_path, null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
  
    
    def __str__(self):
        return self.name

    @property
    def all_exams_ready(self):
        exams = self.exams_patient.all()
        for exam in exams:
            if exam.exam_status != 'pronto':
                return False
        return True
        

    @property
    def has_pending_exams(self):
        exams = self.exams_patient.all()
        for exam in exams:
            if exam.exam_status == 'Pendente':
                return True
        return False

    @property
    def has_collected_exams(self):
        exams = self.exams_patient.all()
        for exam in exams:
            if exam.exam_status == 'Coletado':
                return True
        return False

    @property
    def has_waiting_exams(self):
        exams = self.exams_patient.all()
        for exam in exams:
            if exam.exam_status == 'Aguardando resultado':
                return True
        return False

    @property
    def has_ready_exams(self):
        return self.exams_patient.filter(exam_status='pronto').exists()
    
