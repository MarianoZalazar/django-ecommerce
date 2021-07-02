from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomerModel)
admin.site.register(ProductModel)
admin.site.register(OrderItemModel)
admin.site.register(OrderModel)
admin.site.register(ShippingModel)