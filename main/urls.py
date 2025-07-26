from django.urls import path
from .views import index, ProductCreateView, product_detail

urlpatterns = [
    path('', index, name='index'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path("create/", ProductCreateView.as_view(), name='create'),

]