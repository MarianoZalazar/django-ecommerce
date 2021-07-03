from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitemmodel_set.all()
        cart_items = order.get_order_quantity
    else:
        items = []
        order = {'get_order_total': 0, 'get_order_quantity': 0}
        cart_items = order['get_order_quantity']
    products = ProductModel.objects.all()[:8]
    context = {'products': products, 'order': order, 'cart_items': cart_items}
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
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_order_quantity
    else:
        order = {'get_order_total': 0, 'get_order_quantity': 0}
        cart_items = order['get_order_quantity']
        
    products = ProductModel.objects.all()
    context = {'products': products, 'order': order, 'cart_items': cart_items}
    
    return render(request, 'store/store.html', context)

def product(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_order_quantity
    else:
        order = {'get_order_total': 0, 'get_order_quantity': 0}
        cart_items = order['get_order_quantity']
        
    product = ProductModel.objects.get(pk=pk)
    context = {'product': product, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/product.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitemmodel_set.all()
        cart_items = order.get_order_quantity
    else:
        items = []
        order = {'get_order_total': 0, 'get_order_quantity': 0}
        cart_items = order['get_order_quantity']
        
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)
    
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitemmodel_set.all()
        cart_items = order.get_order_quantity
    else:
        items = []
        order = {'get_order_total': 0, 'get_order_quantity': 0}
        cart_items = order['get_order_quantity']
        
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer = request.user.customermodel
    product = ProductModel.objects.get(id=productId)
    
    order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItemModel.objects.get_or_create(product=product, order=order)
    
    if action == "add":
        order_item.quantity = order_item.quantity + 1
    elif action == "remove":
        order_item.quantity = order_item.quantity - 1
        
    order_item.save()
    
    if order_item.quantity <= 0:
        order_item.delete()
        
    return JsonResponse('item was added', safe=False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customermodel
        order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
        total = float(data['userData']['total'])
        order.transaction_id = transaction_id
        if total == float(order.get_order_total):
            order.complete = True
        order.save()
        
        ShippingModel.objects.create(customer=customer, order=order, **data['shippingData'])
    else:
        print('User not logged in')
        
    
    return JsonResponse('Order Processed', safe=False)