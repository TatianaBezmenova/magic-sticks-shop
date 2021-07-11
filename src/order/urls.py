from django.urls import path
from .views import OrderFormView, OrderListView

app_name = 'order'

urlpatterns = [
    path('form', OrderFormView.as_view(), name='order_form'),
    path('my', OrderListView.as_view(), name='my'),
]
