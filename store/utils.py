import json
from .models import *

def get_order(request):
    if request.user.is_authenticated:
        return user_order(request)
    else:
        return guest_order(request)

def user_order(request):
    customer = request.user.customermodel
    order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
    
    return customer, order

def guest_order(request):
    data = json.loads(request.body)
    email = data['userData']['email']
    first_name = data['userData']['first_name']
    last_name = data['userData']['last_name']
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
        product = ProductModel.objects.get(id=item['product']['id'])
        
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
    cart = json.loads(request.COOKIES.get('cart', {}))
    items = []
    order = {'get_order_total': 0, 'get_order_quantity': 0}
    cart_items = order['get_order_quantity']
    try: 
        for product in cart:
            #In case a product is removed from the store while it's on a guest cart
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
                #TODO Delete product from cart in cookies
                del cart[product]
                print('Product deleted')
    except:
        pass
    return items, order, cart_items

def user_cart(request):
    customer = request.user.customermodel
    order, created = OrderModel.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitemmodel_set.all()
    cart_items = order.get_order_quantity
    return items, order, cart_items