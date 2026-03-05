from django.db import models

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=True)
    phone = models.CharField(max_length=255, null=False, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=True)
    cnpj = models.CharField(max_length=255, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
