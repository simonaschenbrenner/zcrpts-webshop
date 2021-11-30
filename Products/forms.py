from django import forms
from .models import Product, Comment


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'subtitle', 'author', 'type', 'pages', 'date_published']
        widgets = {
            'type': forms.Select(choices=Product.PRODUCT_TYPES),
            'myuser': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'myuser': forms.HiddenInput(),
            'book': forms.HiddenInput(),
        }
