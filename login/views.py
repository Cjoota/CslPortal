
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpRequest
from django.views import View

class LoginView(View):
    def get(self, request: HttpRequest):
        login_form = AuthenticationForm()
        return render(request, 'login.html', context={'login_form': login_form})
    
    def post(self, request: HttpRequest):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('patients')
        else:
            login_form = AuthenticationForm()
            error_message = 'Usuário ou senha inválidos'
            return render(request, 'login.html', context={'login_form': login_form, 'error_message': error_message})

class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect('login')
    
    def post(self, request: HttpRequest):
        logout(request)
        return redirect('login')