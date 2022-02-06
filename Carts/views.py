from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import PaymentForm
from .models import Cart, ShoppingCartItem


def show_shopping_cart(request):

    if request.method == 'POST':
        if 'empty' in request.POST:
            Cart.objects.get(myuser=request.user).delete()
            context = {
                'shopping_cart_is_empty': True,
                'shopping_cart_items': None,
                'total': 0,
            }
            return render(request, 'shopping-cart.html', context)
        elif 'pay' in request.POST:
            return redirect('shopping-cart-pay')

    else:  # request.method == 'GET'
        shopping_cart_is_empty = True
        shopping_cart_items = None
        total = Decimal(0.0)
        myuser = request.user
        if myuser.is_authenticated:
            shopping_carts = Cart.objects.filter(myuser=myuser)
            if shopping_carts:
                shopping_cart = shopping_carts.first()
                shopping_cart_is_empty = False
                shopping_cart_items = ShoppingCartItem.objects.filter(
                    shopping_cart=shopping_cart)
                total = shopping_cart.get_total()

        context = {
            'shopping_cart_is_empty': shopping_cart_is_empty,
            'shopping_cart_items': shopping_cart_items,
            'total': total,
        }
        return render(request, 'shopping-cart.html', context)


@login_required(login_url='/useradmin/login/')
def pay(request):
    form = None
    shopping_cart_is_empty = True
    paid = False
    total = 0
    count_license_keys = 0
    products = []

    shopping_carts = Cart.objects.filter(myuser=request.user)
    if shopping_carts:
        form = PaymentForm()
        shopping_cart_is_empty = False
        shopping_cart = shopping_carts.first()
        total = shopping_cart.get_total()
        shopping_cart_items = ShoppingCartItem.objects.filter(
            shopping_cart=shopping_cart)
        for item in shopping_cart_items:
            products.append(item.product)
            count_license_keys += item.quantity

    if request.method == 'POST':
        myuser = request.user
        form = PaymentForm(request.POST)
        form.instance.myuser = myuser
        if form.is_valid():
            form.save()
            if shopping_carts:
                Cart.objects.get(myuser=myuser).delete()  # Empty shopping cart
            shopping_cart_is_empty = True
            paid = True
        else:
            print(form.errors)
            messages.error(request, 'Payment could not be processed')

    context = {
        'payment_form': form,
        'shopping_cart_is_empty': shopping_cart_is_empty,
        'paid': paid,
        'total': total,
        'count_license_keys': count_license_keys,
        'products': products
    }
    return render(request, 'pay.html', context)
