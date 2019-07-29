from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,AbstractUser

class UserProfile(AbstractUser):
    telephone = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    birth_date = models.DateField(auto_now=False,null=True,blank=True)
    profile_picture = models.ImageField(default='profile_pictures/default.jpg', upload_to='profile_pictures/')    