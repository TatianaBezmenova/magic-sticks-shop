from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.db.transaction import atomic

from .models import Product, ProductType

import logging

log = logging.getLogger(__name__)


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = context['object']
        context['more_products'] = Product.public_objects.filter(type=product.type).exclude(id=product.id)[:10]
        return context


# def product_detail(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     more_products = Product.public_objects.filter(type=product.type).exclude(id=product.id)[:10]
#     return render(request, 'product/product_detail.html', {
#         'object': product,
#         'more_products': more_products,
#     })

class ProductListView(ListView):
    model = Product
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('type')

        if 'type' in self.request.GET:
            queryset = queryset.filter(type_id=self.request.GET['type'])
        if 'price_start' in self.request.GET:
            queryset = queryset.filter(price__gte=self.request.GET['price_start'])
        if 'price_end' in self.request.GET:
            queryset = queryset.filter(price__lte=self.request.GET['price_end'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['product_type_list'] = ProductType.objects.all()
        return context


class ProductAddView(View):
    def get(self, request, *args, **kwargs):
        product_type_list = ProductType.objects.all()
        return render(request, 'product/product_add.html', {
            'product_type_list': product_type_list,
        })

    def post(self, request, *args, **kwargs):
        params = request.POST
        with atomic() as trn:
            obj = {
                'type': ProductType.objects.get(id=int(params['type'])),
                'name': params['name'],
                'price': float(params['price'])
            }
            Product.objects.create(**obj)

        return self.get(request, *args, **kwargs)


def product_type_detail(request, slug):
    product_type = get_object_or_404(ProductType, slug=slug)
    product_list = Product.public_objects.filter(type=product_type)[:10]
    return render(request, 'product/product_type_detail.html', {
        'object': product_type,
        'product_list': product_list,
    })


def cheapest_products_in_type(request, slug):
    product_type = get_object_or_404(ProductType, slug=slug)
    product_list = Product.public_objects.filter(type=product_type).order_by('price')[:50]
    return render(request, 'product/cheapest_products_in_type.html', {
        'object': product_type,
        'product_list': product_list,
    })
