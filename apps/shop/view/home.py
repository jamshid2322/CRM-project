from django.shortcuts import render, redirect
from django.http.response import Http404


def home(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('register_login')
    if user.role == 'admin':
        return redirect('custom_admin')
    if user.role == 'shop':
        return redirect('shop')
    raise Http404()