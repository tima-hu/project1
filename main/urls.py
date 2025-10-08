from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_role, name='choose_role'),
    path('products/', views.product_list, name='product_list'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/add_ajax/<int:product_id>/', views.cart_add_ajax, name='cart_add_ajax'),
    path('cart/remove_ajax/<int:product_id>/', views.cart_remove_ajax, name='cart_remove_ajax'),

    path('order/create/', views.order_create, name='order_create'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    path('profile/seller/', views.profile_seller_view, name='profile_seller'),
    path('profile/buyer/', views.profile_buyer, name='profile_buyer'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    path('seller/purchases/', views.seller_purchases, name='seller_purchases'),
    path('live-search/', views.live_search, name='live_search'),
    path('chat/', views.community_chat, name='chat'),
]
