from django.db import models
from django.conf import settings
from items.models import Item

class ItemComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.TextField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True)


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='messages_from_me')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='messages_to_me')
    message = models.CharField(max_length=180)
    seen = models.DateField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
