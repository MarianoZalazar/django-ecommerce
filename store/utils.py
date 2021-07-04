import json
from .models import *

def get_cart(request):
    if request.user.is_authenticated:
        return user_cart(request)
    else:
        return cookie_cart(request)

def cookie_cart(request):
    cart = json.loads(request.COOKIES.get('cart', {}))
    items = []
    order = {'get_order_total': 0, 'get_order_quantity': 0}
    cart_items = order['get_order_quantity']
    for product in cart:
        try:
            quantity = cart[product]['quantity']
            cart_items += quantity
            product_cart = ProductModel.objects.get(id=product)
            total = (product_cart.price) * quantity
            order['get_order_total'] += total
            order['get_order_quantity']  += quantity
            
            item = {
                'product':{
                    'id': product_cart.id,
                    'name': product_cart.name,
                    'price': product_cart.price,
                    'imageURL': product_cart.imageURL
                },
                'quantity': quantity,
                'get_total': total
            }
            items.append(item)
        except:
            del cart[product]
            print('Product deleted')
    return items, order, cart_items

def user_cart(request):
    customer = request.user.customermodel
    order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitemmodel_set.all()
    cart_items = order.get_order_quantity
    return items, order, cart_items