from django.contrib import admin

# Register your models here.
from .forms import ProductForm
from .models import Product, Picture, Comment, Review


class ProductPictureAdmin(admin.StackedInline):
    model = Picture


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPictureAdmin]

    class Meta:
        model = Product


@admin.register(Picture)
class ProductPictureAdmin(admin.ModelAdmin):
    pass


# Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'product', 'timestamp', 'is_flagged', 'myuser', 'rate')
    list_filter = ('timestamp', 'is_flagged')
    search_fields = ('title', 'product', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Review)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'product', 'timestamp', 'rate', 'myuser')
    list_filter = ('timestamp', 'rate')
    search_fields = ('title', 'product', 'text', 'rate')
    actions = ['approve_rating']

    def approve_rating(self, request, queryset):
        queryset.update(active=True)
