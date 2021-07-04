from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomerModel(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    
    def __str__(self):
        return self.name
    
class ProductModel(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=400, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
        
        
class OrderModel(models.Model):
    customer = models.ForeignKey(CustomerModel,on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.id)
    
    @property
    def get_order_total(self):
        orderitems = self.orderitemmodel_set.all()
        total = sum([orderitem.get_total for orderitem in orderitems])
        return total
    
    @property
    def get_order_quantity(self):
        orderitems = self.orderitemmodel_set.all()
        quantity = sum([orderitem.quantity for orderitem in orderitems])
        return quantity
    
class OrderItemModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OrderModel, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        return self.product.price * self.quantity    
class ShippingModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderModel, on_delete=models.SET_NULL, null=True)    
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
