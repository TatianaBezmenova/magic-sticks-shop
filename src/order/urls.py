from django.urls import path
from .views import OrderFormView

app_name = 'order'

urlpatterns = [
    path('my', OrderFormView.as_view(), name='order_form'),
]
