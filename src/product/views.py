from django.shortcuts import render
from .models import Product, ProductType


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    more_products = Product.objects.filter(type=product.type).exclude(id=product.id)
    return render(request, 'product/product_detail.html', {
        'object': product,
        'more_products': more_products,
    })

def product_type(request, pk):
    product_type = ProductType.objects.get(id=pk)
    products = Product.objects.filter(type=product_type)
    return render(request, 'product/product_type.html', {
        'product_type': product_type,
        'products': products,
    })
