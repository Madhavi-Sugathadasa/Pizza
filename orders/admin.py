from django.contrib import admin

# Register your models here.
from .models import Menu_Type, Menu_Item, Topping, Addition, Cart, Order, Order_Item

# Register your models here.
admin.site.register(Menu_Type)
admin.site.register(Menu_Item)
admin.site.register(Topping)
admin.site.register(Addition)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Order_Item)
