from django import forms
from .models import Product, Comment


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'version', 'short_description', 'long_description', 'file', 'pdf']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['title', 'text']
        widgets = {
            'myuser': forms.HiddenInput(),
            'product': forms.HiddenInput(),
        }
