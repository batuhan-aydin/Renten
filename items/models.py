from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50)   


class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.FloatField()
    picture = models.ImageField(upload_to='item_pictures')
    is_available = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    

class ItemRental(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    hirer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
