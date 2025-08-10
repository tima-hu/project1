

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product
from .cart import Cart

def product_list(request):
    q = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    if q:
        products = products.filter(Q(title__icontains=q) | Q(description__icontains=q))

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product_list.html', {
        'page_obj': page_obj,
        'query': q,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'product_detail.html', {'product': product})

@require_POST
def cart_add_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1

    cart = Cart(request)
    cart.add(product=product, quantity=qty)
    return JsonResponse({
        'success': True,
        'cart_count': len(cart),
        'cart_total': str(cart.get_total_price())
    })

@require_POST
def cart_remove_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return JsonResponse({
        'success': True,
        'cart_count': len(cart),
        'cart_total': str(cart.get_total_price())
    })

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': list(cart),
        'total_price': cart.get_total_price()
    })

@require_POST
def checkout(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')

def live_search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        matches = Product.objects.filter(Q(title__icontains=q) | Q(description__icontains=q)).order_by('title')[:10]
        for p in matches:
            results.append({'id': p.id, 'name': p.title, 'price': str(p.price)})
    return JsonResponse({'results': results})
