from referrals.models import Referrals
from referrals.forms import NewReferralForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
  
@method_decorator(login_required(login_url='login'), name='dispatch')
class ReferralsView(ListView):
    model = Referrals
    template_name = 'referrals.html'
    context_object_name = 'referrals'
    ordering = ['-created_at']
    
    def get_queryset(self):
        referrals = Referrals.objects.all()
        if self.request.user.is_superuser:
            referrals = referrals.all().order_by('-created_at')
        else:
            if self.request.user.company_name:
                referrals = referrals.filter(company_name=self.request.user.company_name).order_by('-created_at')
            else:
                referrals = referrals.none()
        return referrals
   
     
@method_decorator(login_required(login_url='login'), name='dispatch')
class NewReferralView(CreateView):
    model = Referrals
    form_class = NewReferralForm
    template_name = 'new_referrals.html'
    success_url = '/referrals/'
    
    def get_initial(self):
        initial = super().get_initial()
        initial['company_name'] = self.request.user.company_name
        return initial
    