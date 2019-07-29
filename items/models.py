from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    COLORS = (
        ('S', 'success'),
        ('P', 'primary'),
        ('I', 'info'),
        ('W', 'warning'),
        ('D', 'danger'),
        ('A', 'dark'),
        ('E', 'secondary'),
        ('L', 'light')
    )

    ICONS = (
        ('T', 'mobile-alt'),
        ('B', 'book'),
        ('M', 'music'),
        ('C', 'fa-car'),
        ('H', 'home'),
        ('A', 'basketball-ball'),
        ('E', 'headphones'),
        ('D', 'baby-carriage'),
    )
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=1, choices=COLORS, default='P')
    icon = models.CharField(max_length=1, choices=ICONS, default='B')

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name    


class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='items')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    price = models.FloatField()
    picture = models.ImageField(upload_to='item_pictures/', default="item_pictures/default.jpg")
    is_available = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='items')

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Item, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    

class ItemRental(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    hirer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fulfilled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

