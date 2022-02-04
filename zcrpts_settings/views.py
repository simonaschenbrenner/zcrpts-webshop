from Carts.models import Cart
from Products.models import Product
from Products.forms import SearchForm
from django.shortcuts import render


def home(request, **kwargs):
    count = 0
    if request.user.is_authenticated:
        shopping_carts = Cart.objects.filter(myuser=request.user)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
            count = shopping_cart.get_number_of_items()

    context = {
        'count_shopping_cart_items': count,
        'featured_product_list': Product.objects.filter(featured=True),
    }
    return render(request, 'home.html', context)
