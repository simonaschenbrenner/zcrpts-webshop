from django import forms
from .models import Product, Comment, Picture


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'version', 'short_description', 'long_description', 'image', 'pdf', 'price']
        widgets = {
            'myuser': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['title', 'text']
        widgets = {
            'myuser': forms.HiddenInput(),
            'product': forms.HiddenInput(),
        }


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['picture']
        widgets = {
            'product': forms.HiddenInput(),
            'order': forms.HiddenInput(),
            'picture': forms.ClearableFileInput(attrs={'multiple': True})
        }