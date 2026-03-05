from django import forms
from django.db import models
from datetime import datetime
from referrals.models import Referrals

class ExamType(models.TextChoices):
    ADMISSIONAL = 'admissional'
    DEMISSIONAL = 'demissional'
    PERIODICO = 'periodico'
    RETORNO_A_FUNÇÃO = 'retorno_a_funcao'
    MUDANÇA_DE_RISCOS = 'mudanca_de_risco'


class NewReferralForm(forms.ModelForm):
    class Meta:
        model = Referrals
        fields = ['employee_name', 'employee_cpf', 'employee_birth_date', 'employee_function', 'employee_sector', 'exam_type', 'adm_date', 'company_name']
        widgets = {
            'employee_birth_date': forms.DateInput(attrs={'type': 'date'}),
            'adm_date': forms.DateInput(attrs={'type': 'date'}),
            'exam_type': forms.Select(choices=ExamType.choices),
            'company_name': forms.HiddenInput(),
        }
        labels = {
            'employee_name': 'Nome do Colaborador',
            'employee_cpf': 'CPF do Colaborador',
            'employee_birth_date': 'Data de Nascimento do Colaborador',
            'employee_function': 'Função do Colaborador',
            'employee_sector': 'Setor do Colaborador',
            'exam_type': 'Tipo de Exame',
            'adm_date': 'Data de Admissão do Colaborador',
        }
        error_messages = {
            'employee_name': {
                'required': 'O nome do colaborador é obrigatório',
            },
            'employee_cpf': {
                'required': 'O CPF do colaborador é obrigatório',
            },
        }
        
    def clean_employee_birth_date(self):
        birth_date = self.cleaned_data.get('employee_birth_date')
        if birth_date > datetime.now().date():
            self.add_error('employee_birth_date', 'A data de nascimento não pode ser maior que a data atual')
        age = datetime.now().year - birth_date.year
        if age < 18:
            self.add_error('employee_birth_date', 'O colaborador deve ter pelo menos 18 anos')
        return birth_date
    
    def clean_employee_cpf(self):
        import re
        from validate_docbr import CPF
        validator = CPF()
        cpf = self.cleaned_data.get('employee_cpf')
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            self.add_error('employee_cpf', 'O CPF deve estar no formato 000.000.000-00')
        if not validator.validate(cpf):
            self.add_error('employee_cpf', 'O CPF é inválido')
        return cpf
    
    def clean_adm_date(self):
        adm_date = self.cleaned_data.get('adm_date')
        if adm_date > datetime.now().date():
            self.add_error('adm_date', 'A data de admissão não pode ser maior que a data atual')
        return adm_date
    
    