from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "price", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,
    max_num=10,
    can_delete=True
)

class OrderForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Адрес доставки")
    phone = forms.CharField(max_length=20, label="Телефон")
