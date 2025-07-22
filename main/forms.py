from django import forms
from .models import Product  # Импорт только нужной модели

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'category', 'price']
