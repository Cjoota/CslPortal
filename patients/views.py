from patients.models import Patient
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, OuterRef
from django.http import HttpResponseForbidden
from django.http import FileResponse
from exams.models import Exam
     
@method_decorator(login_required(login_url='login'), name='dispatch')
class PatientView(ListView):
    model = Patient
    template_name = 'patients.html'
    context_object_name = 'patients'
    ordering = ['-created_at']

    def get_queryset(self):
        patient_request = self.request.GET.get('patient')
        # Pacientes com algum exame pendente aparecem primeiro
        pendente_subquery = Exam.objects.filter(
            patient_id=OuterRef('pk'),
            exam_status='pendente',
        )
        patients = (
            Patient.objects
            .select_related('company', 'company__sub_company')
            .prefetch_related('exams_patient')
            .annotate(has_pending=Exists(pendente_subquery))
        )
        if self.request.user.is_superuser:
            patients = patients.all()
        else:
            # Subcompania logada: pacientes de todas as empresas que apontam para essa subcompania
            if self.request.user.sub_company:
                patients = patients.filter(company__sub_company=self.request.user.sub_company)
            elif self.request.user.company:
                patients = patients.filter(company=self.request.user.company)
            else:
                patients = patients.none()

        if patient_request:
            patients = patients.filter(name__icontains=patient_request)
        # Pendentes primeiro, depois por data de criação (mais recente primeiro)
        return patients.order_by('-has_pending', '-created_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = self.request.user.company_name if self.request.user.company_name else self.request.user.sub_company
        return context 
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    context_object_name = 'patient'
    
    def get_object(self):
        patient = super().get_object()
        if self.request.user.is_superuser:
            return patient
        if self.request.user.sub_company:
            if patient.company.sub_company_id != self.request.user.sub_company_id:
                raise PermissionDenied("Você não tem permissão para ver este paciente.")
        elif self.request.user.company and patient.company != self.request.user.company:
            raise PermissionDenied("Você não tem permissão para ver este paciente.")
        return patient

    def get_queryset(self):
        qs = (
            Patient.objects
            .select_related('company', 'company__sub_company')
            .prefetch_related('exams_patient')
        )
        if self.request.user.is_superuser:
            return qs.all()
        if self.request.user.sub_company:
            return qs.filter(company__sub_company=self.request.user.sub_company)
        if self.request.user.company:
            return qs.filter(company=self.request.user.company)
        return qs.none()

@login_required(login_url='login')
def open_exam_file(request, patient_id):
    patient = Patient.objects.select_related('company', 'company__sub_company').get(pk=patient_id)

    # REGRA DE OURO LGPD: Verifique se a empresa/subcompania logada é a dona do exame
    if request.user.sub_company:
        if not patient.company_id or patient.company.sub_company_id != request.user.sub_company_id:
            return HttpResponseForbidden("Você não tem permissão para ver este exame.")
    elif request.user.company and patient.company != request.user.company:
        return HttpResponseForbidden("Você não tem permissão para ver este exame.")

    # Caminho absoluto no servidor
    path_to_file = patient.exam_path
    
    # Abre o arquivo de forma segura
    response = FileResponse(path_to_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{patient.name}_exame.pdf"'
    
    return response