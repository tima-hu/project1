from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Seller

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)  # ✅ важно request.FILES для аватара
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите на сайт.')
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)

                if not remember_me:
                    request.session.set_expiry(0)

                messages.success(request, f'Добро пожаловать, {username}!')
                next_url = request.GET.get('next') or '/'
                return redirect(next_url)
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    return LogoutView.as_view(next_page='product_list')(request)
