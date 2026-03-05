from django.db import models

# Create your models here.
class Referrals(models.Model):
    id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=255, null=False)
    employee_cpf = models.CharField(max_length=15, null=False)
    employee_birth_date = models.DateField(null=False)
    employee_function = models.CharField(max_length=255, null=False)
    employee_sector = models.CharField(max_length=255, null=False)
    company_name = models.CharField(max_length=255, null=False)
    exam_type = models.CharField(max_length=255, null=False)
    adm_date = models.DateField(null=True)
    done = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.employee_name
    