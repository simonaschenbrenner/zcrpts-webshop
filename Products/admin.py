from django.contrib import admin

# Register your models here.
from .models import Product, Comment


# class ProductPictureAdmin(admin.StackedInline):
#     model = Picture


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # inlines = [ProductPictureAdmin]

    class Meta:
        model = Product


# @admin.register(Picture)
# class ProductPictureAdmin(admin.ModelAdmin):
#     pass


# Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'product', 'timestamp', 'is_flagged', 'rate', 'myuser')
    list_filter = ('timestamp', 'is_flagged')
    search_fields = ('title', 'product', 'text')
    fields = ['is_flagged']
    # actions = ['approve_comments']
    #
    # def approve_comments(self, request, queryset):
    #     queryset.update(active=True)
