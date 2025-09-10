from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import Seller
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите на сайт.')
            return redirect('login')
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
                auth_login(request, user)  # ✅ используем auth_login, чтобы не было конфликта имён
                
                if not remember_me:
                    request.session.set_expiry(0)  # Сессия закончится при закрытии браузера

                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def user_logout(request):
    return LogoutView.as_view(next_page='product_list')(request, user=request.user)


# def create_seller(request):
#     if request.method == 'POST':
#         store_name = request.POST.get('store_name')
#         if store_name:
#             seller = Seller.objects.create(user=request.user, store_name=store_name)
#             messages.success(request, 'Вы успешно стали продавцом!')
#             return redirect('profile_seller')
#         else:
#             messages.error(request, 'Пожалуйста, введите название магазина.')
#     return render(request, 'create_seller.html')

