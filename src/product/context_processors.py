from .models import ProductType

def categories(request):
    return {
        'categories': ProductType.objects.order_by('name').all()
    }