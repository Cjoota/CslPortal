from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from login.models import Company

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'company', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'company')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Empresa', {'fields': ('company',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Grupos', {'fields': ('groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'company', 'password1', 'password2'),
        }),
    )


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cnpj', 'password', 'created_at')
    search_fields = ('name', 'cnpj', 'password')


admin.site.register(Company, CompanyAdmin)
