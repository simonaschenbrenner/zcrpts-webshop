from Products.models import Product
from django.shortcuts import render


def home(request, **kwargs):
    context = {
        'featured_product_list': Product.objects.filter(featured=True),
    }
    return render(request, 'home.html', context)
