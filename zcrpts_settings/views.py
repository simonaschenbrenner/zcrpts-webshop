from Carts.models import Cart
from Products.forms import SearchForm
from django.shortcuts import render

def home(request, **kwargs):
    count = 0
    if request.user.is_authenticated:
        shopping_carts = Cart.objects.filter(myuser=self)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
            count = shopping_cart.get_number_of_items()
    return count

    context = {'search_form': SearchForm}
    return render(request, 'home.html', context)