from patients.models import Patient
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.http import FileResponse
     
@method_decorator(login_required(login_url='login'), name='dispatch')
class PatientView(ListView):
    model = Patient
    template_name = 'patients.html'
    context_object_name = 'patients'
    ordering = ['-created_at']

    def get_queryset(self):
        patient_request = self.request.GET.get('patient')
        patients = Patient.objects.select_related('company').prefetch_related('exams_patient').all()
        if self.request.user.is_superuser:
            patients = patients.all().order_by('-created_at')
        else:
            if self.request.user.company:
                patients = patients.filter(company=self.request.user.company).order_by('-created_at')
            else:
                patients = patients.none()
        if patient_request:
            patients = patients.filter(name__icontains=patient_request).order_by('name')
        return patients
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = self.request.user.company_name or ''
        return context 
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    context_object_name = 'patient'
    
    def get_object(self):
        patient = super().get_object()
        if self.request.user.company and patient.company != self.request.user.company:
            raise PermissionDenied("Você não tem permissão para ver este paciente.")
        return patient
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset().all()
        if self.request.user.company:
            return super().get_queryset().filter(company=self.request.user.company)
        return super().get_queryset().none()

@login_required(login_url='login')
def open_exam_file(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    
    
    # REGRA DE OURO LGPD: Verifique se a empresa logada é a dona do exame
    if request.user.company and patient.company != request.user.company:
        return HttpResponseForbidden("Você não tem permissão para ver este exame.")

    # Caminho absoluto no servidor
    path_to_file = patient.exam_path
    
    # Abre o arquivo de forma segura
    response = FileResponse(path_to_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{patient.name}_exame.pdf"'
    
    return response