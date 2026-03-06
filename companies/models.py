from django.db import models


class SubCompany(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    cnpj = models.CharField(max_length=255, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name




class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=True)
    phone = models.CharField(max_length=255, null=False, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=True)
    cnpj = models.CharField(max_length=255, null=False, blank=False, unique=True)
    sub_company = models.ForeignKey(SubCompany, on_delete=models.PROTECT, related_name='companies', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

    