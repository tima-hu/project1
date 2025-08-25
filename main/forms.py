from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import User, Product, ProductImage


# ===========================
#   ФОРМА РЕГИСТРАЦИИ
# ===========================
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        label="Роль"
    )
    phone = forms.CharField(
        required=False,
        label="Телефон",
        widget=forms.TextInput(attrs={"placeholder": "+7..."})
    )
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = User
        fields = ("username", "email", "role", "phone", "avatar", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username



# ===========================
#   ФОРМА ТОВАРА
# ===========================
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "price", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
        }


# ===========================
#   ФОРМА КАРТИНОК ТОВАРА
# ===========================
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]


# ===========================
#   ФОРМСЕТ ДЛЯ КАРТИНОК
# ===========================
ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,
    max_num=10,
    can_delete=True
)
