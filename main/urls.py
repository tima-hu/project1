from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add_ajax, name='cart_add_ajax'),
    path('cart/remove/<int:product_id>/', views.cart_remove_ajax, name='cart_remove_ajax'),
    path('checkout/', views.checkout, name='checkout'),
    path('live-search/', views.live_search, name='live_search'),
    # path('create/', )
]
