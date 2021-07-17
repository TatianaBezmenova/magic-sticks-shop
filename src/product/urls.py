from django.urls import path
from .views import product_type_detail, cheapest_products_in_type, ProductDetailView, ProductListView, ProductAddView

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product_add/', ProductAddView.as_view(), name='product_add'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/', product_type_detail, name='product_type_detail'),
    path('<slug:slug>/cheapest/', cheapest_products_in_type, name='cheapest_products_in_type'),
]
