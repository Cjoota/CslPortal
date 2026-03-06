from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Usuário customizado: sem first_name/last_name, com company (FK para companies.Company)."""
    first_name = None
    last_name = None
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='users',
    )
    sub_company = models.ForeignKey(
        'companies.SubCompany',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='users',
    )

    class Meta:
        db_table = 'login_user'

    @property
    def company_name(self):
        """Nome da empresa do usuário (ou None se superuser sem company)."""
        if self.is_superuser:
            return "ADMINISTRADOR"
        return self.company.name if self.company else self.sub_company.name if self.sub_company else None

    @property
    def sub_company_name(self):
        """Nome da subempresa do usuário (ou None se superuser sem subempresa)."""
        if self.is_superuser:
            return None
        return self.sub_company.name

