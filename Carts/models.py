from django.conf import settings
from django.core.validators import MinValueValidator
from Products.models import Product
from decimal import Decimal
from django.db import models
from django.utils import timezone


# TODO Umbennenen? Repräsentiert ein Produkt im Warenkorb, Warenkorb ist Menge aller Einträge zu einem User

class Cart(models.Model):
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ['myuser', 'product']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def add_item(myuser, product):
        # Get existing shopping cart, or create a new one if none exists
        shopping_carts = Cart.objects.filter(myuser=myuser)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
        else:
            shopping_cart = Cart.objects.create(myuser=myuser)

        # Add item to shopping cart
        product_id = product.id
        product_name = product.get_full_title() + ' '+ product.get_long_description()
        Cart.objects.create(product_id=product_id,
                            product_name=product_name,
                            price=product.price,
                            quantity=1,
                            shopping_cart=shopping_cart,
                            )

    def get_number_of_items(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        return len(shopping_cart_items)

    def get_total(self):
        total = Decimal(0.0)  # Default without Decimal() would be type float!
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        for item in shopping_cart_items:
            total += item.price * item.quantity
        return total

    def __str__(self):
        return self.myuser + ' has ' + self.quantity + ' of ' + self.product.title + ' in their cart'

    def __repr__(self):
        return 'Cart: ' + self.quantity + ' x ' + self.product.title + ' for ' + self.myuser


class ShoppingCartItem(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    shopping_cart = models.ForeignKey(Cart,
                                      on_delete=models.CASCADE,
                                      )


class Payment(models.Model):
    credit_card_number = models.CharField(max_length=19)  # Format: 1234 5678 1234 5678
    expiry_date = models.CharField(max_length=7)  # Format: 10/2022
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(default=timezone.now)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
