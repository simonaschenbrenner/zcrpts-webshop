from decimal import Decimal
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from Products.models import Product


# Whole shopping Cart
class Cart(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    myuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    @staticmethod
    def add_item(myuser, product):
        # Get existing shopping cart, or create a new one if none exists
        shopping_carts = Cart.objects.filter(myuser=myuser)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
        else:
            shopping_cart = Cart.objects.create(myuser=myuser)

        # Add item to shopping cart
        shopping_cart_item = ShoppingCartItem.objects.filter(
            shopping_cart=shopping_cart).filter(product=product).first()
        if shopping_cart_item:
            shopping_cart_item.quantity += 1
            shopping_cart_item.save()
        else:
            ShoppingCartItem.objects.create(product=product,
                                            quantity=1,
                                            shopping_cart=shopping_cart,
                                            )

    def get_number_of_items(self):
        count = 0
        shopping_cart_items = ShoppingCartItem.objects.filter(
            shopping_cart=self)
        for item in shopping_cart_items:
            count += item.quantity
        return count

    def get_total(self):
        total = Decimal(0.0)
        shopping_cart_items = ShoppingCartItem.objects.filter(
            shopping_cart=self)
        for item in shopping_cart_items:
            total += Decimal(item.product.price) * item.quantity
        return total

    def __str__(self):
        # TODO
        return self.myuser.__str__()

    def __repr__(self):
        # TODO
        return self.myuser.__str__()


# One item in shopping cart
class ShoppingCartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    """
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    """
    quantity = models.IntegerField(default=1)
    shopping_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class Payment(models.Model):
    credit_card_number = models.CharField(
        max_length=16,
        validators=[RegexValidator(
            # Source: https://ihateregex.io/expr/credit-card/
            regex=r"(^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|"\
                  r"22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|"\
                  r"(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?"\
                  r":011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)",
            message = "Not a valid credit card number")]
    )

    expiry_date = models.CharField(
        max_length=7,
        validators=[RegexValidator(
            regex=r"[01]?\d{1}/2\d{3}",  # TODO regex
            message="Invalid date, must be in the following format: MM/YYYY")])
    cvc = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(default=timezone.now)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
