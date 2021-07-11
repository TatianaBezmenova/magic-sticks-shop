from django.views.generic import FormView, ListView
from django.urls import reverse_lazy

from .forms import OrderForm
from .models import Order


class OrderFormView(FormView):
    template_name = 'order/order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order:my')

    def form_valid(self, form):
        order = form.save(commit=False)

        if not self.request.user.is_anonymous:
            order.user = self.request.user

        order.save()
        return super().form_valid(form)


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
