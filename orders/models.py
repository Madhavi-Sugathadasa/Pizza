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
