from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from .models import Product, ProductImage, Order, OrderItem, ChatMessage,Cart, CartItem
from .forms import ProductForm, ProductImageFormSet, OrderForm
from decimal import Decimal
from users.models import Seller


@login_required
def community_chat(request):
    
    messages_qs = ChatMessage.objects.select_related("user").order_by("created_at")[:50]
    
    return render(request, "chat.html", {"messages": messages_qs})


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
    
    if hasattr(request.user, 'seller'):
        return redirect("profile_seller")

   
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "profile_buyer.html", {"orders": orders})

@login_required
def product_create(request):
    
    seller, _ = Seller.objects.get_or_create(
        user=request.user
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
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order).select_related("product")

    return render(request, "order_success.html", {
        "order": order,
        "items": items
    })


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related("product")
    total_price = cart.total_price()
    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()
    return redirect("cart")

@login_required
def cart_add_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    total_items = sum(item.quantity for item in cart.items.all())
    return JsonResponse({'success': True, 'cart_total': total_items})


@login_required
def cart_remove_ajax(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()

    total_items = sum(item.quantity for item in cart.items.all())
    return JsonResponse({'success': True, 'cart_total': total_items})

@login_required
def order_create(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')
    total_price = cart.total_price()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user, cart=cart)
            # Можно сохранять адрес и телефон, если добавишь поля в модель Order
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'order_create.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

