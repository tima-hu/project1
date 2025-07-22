from django.urls import path
from .views import index, ProductCreateView


urlpatterns = [
    path('', index, name='index'),
    path("create/", ProductCreateView.as_view(), name='create')
]