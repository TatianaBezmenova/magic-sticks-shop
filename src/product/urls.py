from django.urls import path
from .views import product_detail, product_type_detail, cheapest_products_in_type

app_name = 'product'

urlpatterns = [
    path('<int:pk>/', product_detail, name='product_detail'),
    path('<slug:slug>/', product_type_detail, name='product_type_detail'),
    path('<slug:slug>/cheapest/', cheapest_products_in_type, name='cheapest_products_in_type'),
]
