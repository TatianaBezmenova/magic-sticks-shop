from django.urls import path
from .views import product_detail, product_type

app_name = 'product'

urlpatterns = [
    path('<int:pk>/', product_detail, name='product_detail'),
    path('type/<int:pk>/', product_type, name='product_type'),
]
