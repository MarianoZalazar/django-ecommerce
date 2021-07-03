from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    products = ProductModel.objects.all()
    context = {'products': products}
    return render(request, 'store/index.html', context)

def login(request):
    context = {}
    return render(request, 'store/login.html', context)

def register(request):
    context = {}
    return render(request, 'store/register.html', context)

def reset(request):
    context = {}
    return render(request, 'store/reset.html', context)

def forgot(request):
    context = {}
    return render(request, 'store/forgot.html', context)

def store(request):
    products = ProductModel.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def product(request):
    context = {}
    return render(request, 'store/product.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitemmodel_set.all()
    else:
        items = []
        order = {'get_order_total': 0, 'get_order_quantity': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)
    
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitemmodel_set.all()
    else:
        items = []
        order = {'get_order_total': 0, 'get_order_quantity': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)