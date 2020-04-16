from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Menu_Type(models.Model):
    name = models.CharField(max_length=64)
    display_order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - order:{self.display_order}"

class Menu_Item(models.Model):
    type_id = models.ForeignKey(Menu_Type,on_delete=models.CASCADE,related_name="menu_types")
    item_name = models.CharField(max_length=64)
    image = models.ImageField(upload_to ='Media')
    no_of_toppings = models.IntegerField(default=0)
    is_mult_cat = models.BooleanField(default=False)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.type_id.name} - {self.item_name}"

class Topping(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.name}"

class Addition(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.FloatField(null=True, blank=True)
    large_price = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    
class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id", unique=True)
    date_time = models.DateTimeField()
    basket = models.CharField(max_length=500)
    
    def __str__(self):
        return f"{self.user_id}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    total = models.FloatField()
    date_time = models.DateTimeField()
    status = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    payment_session = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} - {self.user_id} - {self.date_time} - {self.status}"
    
class Order_Item(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_id")
    item_name = models.CharField(max_length=100)
    size = models.CharField(max_length=2, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    
    def __str__(self):
        return f"{self.order_id} - {self.item_name} - {self.quantity}"