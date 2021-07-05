from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import CreateAccountForm
# Create your views here.
def login(request):
    context = {}
    return render(request, 'user/login.html', context)

def register(request):
    context = {}
    return render(request, 'user/register.html', context)

def reset(request):
    context = {}
    return render(request, 'user/reset.html', context)

def forgot(request):
    context = {}
    return render(request, 'user/forgot.html', context)