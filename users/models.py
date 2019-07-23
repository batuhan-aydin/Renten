from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    telephone = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    birthday = models.DateField(auto_now=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pictures')    