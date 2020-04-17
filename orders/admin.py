from django.contrib import admin

# Register your models here.
from .models import Menu_Type, Menu_Item

admin.site.register(Menu_Type)
admin.site.register(Menu_Item)