from django.db import models
from django.conf import settings

# Create your models here.


class CustomerModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.email


class ProductModel(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=400, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_sale = models.BooleanField(default=False, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=8,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)

    def __str__(self):
        return self.name

    #A property decorator make an attribute out of a function
    #That's why they're mentioned in the docs like 'managed attributes'
    #This function tries to get the image for the template
    #it's used to prevent no-images products
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class OrderModel(models.Model):
    customer = models.ForeignKey(CustomerModel,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_order_items(self):
        return self.orderitemmodel_set.all()

    @property
    def get_order_total(self):
        #This a reverse lookup based on the 1 to Many relationship
        #between OrderModel and OrderItemModel
        orderitems = self.orderitemmodel_set.all()
        total = sum([orderitem.get_total for orderitem in orderitems])
        return total

    @property
    def get_order_quantity(self):
        orderitems = self.orderitemmodel_set.all()
        quantity = sum([orderitem.quantity for orderitem in orderitems])
        return quantity


class OrderItemModel(models.Model):
    product = models.ForeignKey(ProductModel,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    order = models.ForeignKey(OrderModel,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        if not self.product.is_sale:
            return self.product.price * self.quantity
        else:
            return self.product.sale_price * self.quantity


class ShippingModel(models.Model):
    customer = models.ForeignKey(CustomerModel,
                                 on_delete=models.SET_NULL,
                                 null=True)
    order = models.ForeignKey(OrderModel, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
