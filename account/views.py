from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import *
from .models import Account
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from store.models import CustomerModel


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    context = {}
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password, backend='account.backends.CaseInsensitiveModelBackend')
            if user is not None:
                login(request, user, backend='account.backends.CaseInsensitiveModelBackend')
                return redirect('/')
        else:
            context['loginform'] = form
    return render(request, 'user/login.html', context)

def register(request, *args, **kwargs):
    
    if request.user.is_authenticated:
        return redirect('/')
    context = {}
    
    if request.POST:
        userform = UserDataForm(request.POST)
        if userform.is_valid():
            email = userform.cleaned_data.get('email')
            raw_password = userform.cleaned_data.get('password2')
            first_name = userform.cleaned_data.get('first_name')
            last_name = userform.cleaned_data.get('last_name') 
            account = Account.objects.create_user(email=email, password=raw_password)
            customer, created = CustomerModel.objects.get_or_create(email=email)
            customer.user = account
            customer.first_name = first_name
            customer.last_name = last_name
            customer.save()
            if account is not None:
                login(request, account, backend='account.backends.CaseInsensitiveModelBackend')            
            destination = kwargs.get('next')
            if destination:
               return(redirect(destination))
            return redirect('/')
        else:
             context['createuserform'] = userform
    
    return render(request, 'user/register.html', context)

def reset(request):
    context = {}
    return render(request, 'user/reset.html', context)

def forgot(request):
    context = {}
    return render(request, 'user/forgot.html', context)

def log_out(request):
    if request.user.is_active:
        logout(request)
    
    return redirect('/')