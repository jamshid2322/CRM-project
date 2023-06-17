from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponseRedirect
from apps.utilis.permisions import UserAuthenticateRequiredMixin


class UserRegisterLogin(View):

    def get(self, request, *args, **kwargs):
        method = request.GET.get('method', 'login')
        match method:
            case 'login':
                return render(request, 'user/login.html')
            
    
    def post(self, request, *args, **kwargs):
        method = request.POST.get('method', 'login')

        match method:
            # case 'register':
            #     return render(request, 'user/register.html')

            case 'login':
                phone = request.POST.get('phone')
                password = request.POST.get('password')
                user = authenticate(request, phone_number=phone, password=password)
                if not user:
                    messages.error(request, 'Invalid Phone number or password')
                    return redirect('register_login')
                login(request, user)
                return redirect("home")

            case 'logout':
                logout(request)
                return redirect("register_login")


