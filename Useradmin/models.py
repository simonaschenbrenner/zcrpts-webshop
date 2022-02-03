from django.contrib.auth.models import AbstractUser
from django.db import models
from Carts.models import Cart


class MyUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True)

    def __str__(self):
        role = "User"
        if self.is_manager:
            role = "Manager"
        if self.is_superuser:
            role = "Admin"
        return self.first_name + ' ' + self.last_name + ' (' + role + ')'

    def __repr__(self):
        return 'User "' + self.username + '": ' + self.__str__()

    def count_shopping_cart_items(self):
        count = 0
        if self.is_authenticated:
            shopping_carts = Cart.objects.filter(myuser=self)
            if shopping_carts:
                shopping_cart = shopping_carts.first()
                count = shopping_cart.get_number_of_items()
        return count
