from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product
from .forms import ProductForm, ProductImageFormSet
from .filters import ProductFilters
from django.views.decorators.http import require_POST

def index(request):
    product = Product.objects.all()
    product_filter = ProductFilters(request.GET, queryset=product)
    return render(request, 'index.html', {'product_filter': product_filter})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm()
        formset = ProductImageFormSet()
    return render(request, 'create.html', {'form': form, 'formset': formset})

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': total
            })
            total_price += total
        except Product.DoesNotExist:
            continue

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

@require_POST
def checkout_view(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart')

def live_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        matches = Product.objects.filter(title__icontains=query).order_by('title')[:10]
        results = [{'id': p.id, 'name': p.title, 'price': p.price} for p in matches]
    return JsonResponse({'results': results})
