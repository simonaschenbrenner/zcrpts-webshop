from django.contrib import admin

# Register your models here.
from .models import Product, Picture


class PostPictureAdmin(admin.StackedInline):
    model = Picture


@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostPictureAdmin]

    class Meta:
        model = Product


@admin.register(Picture)
class PostPictureAdmin(admin.ModelAdmin):
    pass