from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Menu_Type(models.Model):
    name = models.CharField(max_length=64)
    display_order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - order:{self.display_order}"