from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Product, ProductType


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
