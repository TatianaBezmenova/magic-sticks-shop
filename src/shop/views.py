from django.shortcuts import render

from product.models import ProductType


def index(request):
    product_type_list = ProductType.objects.all()
    return render(request, 'shop/index.html', {
        'product_type_list': product_type_list,
    })
