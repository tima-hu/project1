from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from .models import Product, ProductImage, Order, OrderItem, Seller, ChatMessage
from .forms import ProductForm, ProductImageFormSet, CustomUserCreationForm


# ------------------------- ЧАТ -------------------------
@login_required
def community_chat(request):
    messages_qs = list(ChatMessage.objects.select_related("user").order_by("-created_at")[:50])
    messages_qs.reverse()  # чтобы сначала старые
    return render(request, "chat.html", {"messages": messages_qs})


# ------------------------- ПРОФИЛИ -------------------------
@login_required
def profile_seller_view(request):
    seller = getattr(request.user, 'seller', None)
    seller_products = Product.objects.filter(seller=seller) if seller else Product.objects.none()
    return render(request, 'profile_seller.html', {
        'user': request.user,
        'seller': seller,
        'seller_products': seller_products
    })


@login_required
def profile_buyer(request):
    # Если продавец пытается зайти в профиль покупателя → перенаправляем
    if hasattr(request.user, 'seller'):
        return redirect("profile_seller")

    # Все заказы текущего покупателя
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "profile_buyer.html", {"orders": orders})


# ------------------------- РЕГИСТРАЦИЯ -------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Создаем продавца автоматически
            Seller.objects.get_or_create(user=user, defaults={"store_name": f"Магазин {user.username}"})

            # Автоматический вход
            backend = get_backends()[0]
            login(request, user, backend=backend.__class__.__module__ + '.' + backend.__class__.__name__)

            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('product_list')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте правильность данных.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


# ------------------------- ТОВАРЫ -------------------------
@login_required
def product_create(request):
    # Гарантируем, что у пользователя есть продавец
    seller, _ = Seller.objects.get_or_create(
        user=request.user,
        defaults={"store_name": f"Магазин {request.user.username}"}
    )

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()
            messages.success(request, "Товар успешно создан!")
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "product_create.html", {"form": form})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller__user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Товар успешно обновлён!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    return render(request, 'product_form.html', {'form': form, 'formset': formset})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller__user=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удалён!')
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products.order_by('-id'), 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product_list.html', {
        'page_obj': page_obj,
        'query': query
    })


# ------------------------- КОРЗИНА -------------------------
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = quantity * product.price
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': product.price,
            'total': item_total,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@require_POST
def cart_add_ajax(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    return JsonResponse({'success': True, 'cart': cart, 'message': f'Добавлено: {product.name}'})


@require_POST
def cart_remove_ajax(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            cart.pop(key)
        request.session['cart'] = cart
    return JsonResponse({'success': True, 'cart': cart, 'message': f'Удалено: {product.name}'})


# ------------------------- ПРОЧЕЕ -------------------------
class UserLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        password = request.POST.get('password', '')
        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)

        messages.success(request, 'Профиль успешно обновлён!')
        return redirect('profile_seller')

    return render(request, 'profile_edit.html', {'user': user})


@login_required
def seller_purchases(request):
    seller = get_object_or_404(Seller, user=request.user)
    purchases = OrderItem.objects.filter(
        product__seller=seller
    ).select_related('product', 'order', 'order__user')
    return render(request, 'seller_purchases.html', {
        'seller': seller,
        'purchases': purchases,
    })


def live_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = list(Product.objects.filter(name__icontains=query).values('id', 'name'))
    return JsonResponse({'results': results})
@login_required
def choose_role(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role in ["buyer", "seller"]:
            request.user.role = role
            request.user.save()
            if role == "seller":
                return redirect("profile_seller")
            return redirect("profile_buyer")
    return render(request, "choose_role.html")

@login_required
def order_success(request, order_id):
    # Получаем заказ
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Загружаем товары в заказе
    items = OrderItem.objects.filter(order=order).select_related("product")

    return render(request, "order_success.html", {
        "order": order,
        "items": items
    })