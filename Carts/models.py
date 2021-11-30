from datetime import date
from django.conf import settings
from django.db import models
from Products.models import Product


class Cart(models.Model):
    quantity = models.IntegerField()  # Must call function to take effect
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return 'Cart with: ' + self.quantity + 'products'

    def __repr__(self):
        return 'User: ' + self.userID + '| Product: ' + self.productID + '| Quantity: ' + self.quantity
