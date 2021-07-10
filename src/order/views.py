from django.views.generic import FormView

from .forms import OrderForm

class OrderFormView(FormView):
    template_name = 'order/order_form.html'
    form_class = OrderForm
