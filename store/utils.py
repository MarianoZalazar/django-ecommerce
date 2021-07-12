import json
from .models import *

def get_order(request, usershippingform):
    if request.user.is_authenticated:
        return user_order(request)
    else:
        return guest_order(request, usershippingform)

def user_order(request):
    customer = request.user.customermodel
    order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
    
    return customer, order

def guest_order(request, usershippingform):
    email = usershippingform.cleaned_data['email']
    first_name = usershippingform.cleaned_data['first_name']
    last_name = usershippingform.cleaned_data['last_name']
    cart = cookie_cart(request)
    items = cart['items']
    
    #This line uses a get_or_create method to
    #make an unauthenticated customer based on the provided email
    customer, created = CustomerModel.objects.get_or_create(email=email)
    customer.first_name = first_name
    customer.last_name = last_name
    customer.save()
    
    order = OrderModel.objects.create(customer=customer)
    
    for item in items:
        #Check the cookie_cart function to understand the 'item' structure
        try:
            product = ProductModel.objects.get(id=item['product']['id'])
        except:
            continue
        order_item = OrderItemModel.objects.create(order=order, 
                                                    product=product, 
                                                    quantity=item['quantity'])
    return customer, order



def get_cart(request):
    if request.user.is_authenticated:
        return user_cart(request)
    else:
        return cookie_cart(request)

def cookie_cart(request):
    try: 
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_order_total': 0, 'get_order_quantity': 0}
    cart_items = order['get_order_quantity']
    for product in list(cart.keys()):
        #In case a product is removed from the store while it's on a guest cart
        try:
            quantity = cart[product]['quantity']
            cart_items += quantity
            product_cart = ProductModel.objects.get(id=product)
            if product_cart.is_sale:
                total = product_cart.sale_price * quantity
            else:
                total = (product_cart.price) * quantity
            order['get_order_total'] += total
            order['get_order_quantity']  += quantity
            
            item = {
                'product':{
                    'id': product_cart.id,
                    'name': product_cart.name,
                    'price': product_cart.price,
                    'imageURL': product_cart.imageURL,
                    'is_sale': product_cart.is_sale,
                    'sale_price': product_cart.sale_price
                },
                'quantity': quantity,
                'get_total': total
            }
            items.append(item)
        except:
            continue
    return {'items': items, 'order':order, 'cart_items':cart_items, 'cart': cart}

def user_cart(request):
    customer = request.user.customermodel
    order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitemmodel_set.all()
    cart_items = order.get_order_quantity
    return {'items': items, 'order':order, 'cart_items':cart_items, 'cart': None}
