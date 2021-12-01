from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from Products.models import Product

# TODO Umbennenen? Repräsentiert ein Produkt im Warenkorb, Warenkorb ist Menge aller Einträge zu einem User
class Cart(models.Model):
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # TODO MaxValueValidator?
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ['myuser', 'product']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    # TODO
    """
    def get_total_quantity(self, myuser):
        products_in_cart = Cart.objects.filter(myuser=myuser)
        total_quantity = 0
        for product in products_in_cart:
            total_quantity = total_quantity + product.quantity
        return total_quantity
    """

    def __str__(self):
        return self.myuser + ' has ' + self.quantity + ' of ' + self.product.title + ' in their cart'

    def __repr__(self):
        return 'Cart: ' + self.quantity + ' x ' + self.product.title + ' for ' + self.myuser
