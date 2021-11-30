from datetime import date, datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


def get_date_20_years_ago():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    return date(year - 20, month, day)


class MyUser(AbstractUser):
    date_of_birth = models.DateField(default=get_date_20_years_ago())  # Default is 20 years old
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    some_file = models.FileField(upload_to='uploaded_files/', blank=True, null=True)
    is_a_cat = models.BooleanField(default=False)

    def execute_after_login(self):
        if 'Cat' in self.first_name or 'cat' in self.first_name \
                or 'Cat' in self.last_name or 'cat' in self.last_name:
            self.is_a_cat = True
        self.save()

    def has_birthday_today(self):
        return_boolean = False

        now = datetime.now()
        today_month = now.month
        today_day = now.day

        user_month = self.date_of_birth.month
        user_day = self.date_of_birth.day

        if user_month == today_month and user_day == today_day:
            return_boolean = True
        return return_boolean

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + str(self.date_of_birth) + ')'
