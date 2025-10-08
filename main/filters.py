import django_filters
from .models import Product

class ProductFilters(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="name", lookup_expr="icontains", label="Название")
    price_gte = django_filters.NumberFilter(field_name="price", lookup_expr='gte', label="Цена от")
    price_lte = django_filters.NumberFilter(field_name="price", lookup_expr="lte", label="Цена до")

    class Meta:
        model = Product
        fields = ['title', 'price_gte', 'price_lte']
