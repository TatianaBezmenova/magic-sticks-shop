from django.shortcuts import render, get_object_or_404
from .models import Product, ProductType


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    more_products = Product.objects.filter(type=product.type).exclude(id=product.id)[:10]
    return render(request, 'product/product_detail.html', {
        'object': product,
        'more_products': more_products,
    })


def product_type_detail(request, slug):
    product_type = get_object_or_404(ProductType, slug=slug)
    product_list = Product.objects.filter(type=product_type)[:10]
    return render(request, 'product/product_type_detail.html', {
        'object': product_type,
        'product_list': product_list,
    })