from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, label="Роль")
    phone = forms.CharField(required=False, label="Телефон", widget=forms.TextInput(attrs={"placeholder": "+7..."}))
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = User
        fields = ("username", "email", "role", "phone", "avatar", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.phone = self.cleaned_data.get('phone')
        if self.cleaned_data.get('avatar'):
            user.avatar = self.cleaned_data['avatar']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Запомнить меня', required=False)
