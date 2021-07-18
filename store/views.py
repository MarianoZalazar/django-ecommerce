from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import json
import datetime
from .models import *
from .forms import *
from .utils import get_cart, get_order, create_preferences
# Create your views here.


def index(request):
    cart = get_cart(request)
    products_sale = ProductModel.objects.all().filter(is_sale=True)[:8]
    products = ProductModel.objects.all().filter(is_sale=False)[:8]
    context = {
        'items': cart['items'],
        'order': cart['order'],
        'cart_items': cart['cart_items'],
        'products_sale': products_sale,
        'products': products
    }
    return render(request, 'store/index.html', context)


def store(request):
    cart = get_cart(request)
    products = ProductModel.objects.all()
    context = {
        'items': cart['items'],
        'order': cart['order'],
        'cart_items': cart['cart_items'],
        'products': products
    }
    return render(request, 'store/store.html', context)


def product(request, pk):
    cart = get_cart(request)
    product = ProductModel.objects.get(pk=pk)
    context = {
        'items': cart['items'],
        'order': cart['order'],
        'cart_items': cart['cart_items'],
        'product': product
    }
    return render(request, 'store/product.html', context)


def cart(request):
    cart = get_cart(request)
    context = {
        'items': cart['items'],
        'order': cart['order'],
        'cart_items': cart['cart_items']
    }
    response = render(request, 'store/cart.html', context)
    # if (new_cart := cart['cart']) is not None:
    #     response.set_cookie('cart', new_cart)
    return response


def checkout(request):
    cart = get_cart(request)
    context = {
        'items': cart['items'],
        'order': cart['order'],
        'cart_items': cart['cart_items']
    }
    if request.POST:
        usershippingform = UserShippingDataForm(request.POST)
        if usershippingform.is_valid():
            customer, order = get_order(request, usershippingform)
            total = usershippingform.cleaned_data['total']
            order.transaction_id = datetime.datetime.now().timestamp()
            if total == float(order.get_order_total):
                #redirect to payment view
                order.save()
                ShippingModel.objects.create(
                    customer=customer,
                    order=order,
                    city=usershippingform.cleaned_data['city'],
                    state=usershippingform.cleaned_data['state'],
                    zipcode=usershippingform.cleaned_data['zipcode'],
                    address=usershippingform.cleaned_data['address'])
                response = redirect('/payment')
                response.set_cookie('order_id', order.id)
                return response
        else:
            context['usershippingform'] = usershippingform
    return render(request, 'store/checkout.html', context)


def payment(request):
    context = {'error': False}
    try:
        order_id = request.COOKIES['order_id']
        order = OrderModel.objects.get(id=order_id)
        if order.complete == False:
            preference_data = create_preferences(order)
            context['preference'] = preference_data['preference']
            context['PUBLIC_KEY'] = preference_data['PUBLIC_KEY']
        else:
            raise Exception
    except:
        context['error'] = True
    return render(request, 'store/payment.html', context)


def payment_output(request):
    response = redirect('/')
    try:
        data = request.GET
        print(data)
        if data['collection_status'] == 'approved':
            order_id = data['external_reference']
            order = OrderModel.objects.get(id=order_id)
            order.complete = True
            order.save()
            response.set_cookie('cart', {})
    except:
        pass
    return response

#This view is only used by authenticated users
#the updates of a guest's cart are managed by cookies
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customermodel
    product = ProductModel.objects.get(id=productId)

    order, created = OrderModel.objects.get_or_create(customer=customer,
                                                      complete=False)
    order_item, created = OrderItemModel.objects.get_or_create(product=product,
                                                               order=order)

    if action == "add":
        order_item.quantity = order_item.quantity + 1
    elif action == "remove":
        order_item.quantity = order_item.quantity - 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('item was added', safe=False)


def process_order(request):

    if request.POST:
        usershippingform = UserShippingDataForm(request.POST)
        if usershippingform.is_valid():
            customer, order = get_order(request, usershippingform)
            total = usershippingform.cleaned_data['total']
            order.transaction_id = datetime.datetime.now().timestamp()
            if total == float(order.get_order_total):
                order.complete = True
            order.save()
            ShippingModel.objects.create(
                customer=customer,
                order=order,
                city=usershippingform.cleaned_data['city'],
                state=usershippingform.cleaned_data['state'],
                zipcode=usershippingform.cleaned_data['zipcode'],
                address=usershippingform.cleaned_data['address'])
    else:
        context['usershippingform'] = UserShippingDataForm()
    return JsonResponse('Order Processed', safe=False)