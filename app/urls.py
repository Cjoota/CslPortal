"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from login.views import LoginView, LogoutView
from patients.views import PatientView, open_exam_file, PatientDetailView
from referrals.views import NewReferralView, ReferralsView
from privacy_polices.views import privacy_policy
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('painelstaff/admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('patients/', PatientView.as_view(), name='patients'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patients/<int:patient_id>/exam/', open_exam_file, name='open_exam_file'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('new_referral/', NewReferralView.as_view(), name='new_referral'),
    path('referrals/', ReferralsView.as_view(), name='referrals'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


 