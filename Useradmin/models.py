from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        role = "User"
        if self.is_manager:
            role = "Manager"
        if self.is_superuser:
            role = "Admin"
        return self.first_name + ' ' + self.last_name + ' (' + role + ')'

    def __repr__(self):
        return 'User "' + self.username + '": ' + self.__str__()
