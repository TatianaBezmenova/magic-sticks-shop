from django.urls import path
from .views import product_detail, product_type_detail

app_name = 'product'

urlpatterns = [
    path('<int:pk>/', product_detail, name='product_detail'),
    path('<slug:slug>/', product_type_detail, name='product_type_detail')
]
