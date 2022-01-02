from django.contrib import admin
from .models import Cart, ShoppingCartItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(ShoppingCartItem)