from django import forms

from items.models import Category, Item 



class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'picture', 'is_available', 'category']
        