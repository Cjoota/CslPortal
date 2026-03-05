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

    class Meta:
        db_table = 'login_user'

    @property
    def company_name(self):
        """Nome da empresa do usuário (ou None se superuser sem company)."""
        return self.company.name



