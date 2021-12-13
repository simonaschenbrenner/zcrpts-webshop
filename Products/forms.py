from django import forms
from .models import Product, Comment, Picture


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = ['title', 'version', 'short_description', 'long_description', 'pdf', 'image', 'price']
        widgets = {
            'myuser': forms.HiddenInput()
        }

CHOICES =(
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['title', 'text', 'rate']
        widgets = {
            'myuser': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'rate': forms.ChoiceField(
                label='Rating: ',
                choices=CHOICES,
                widget=forms.RadioSelect,
            )

        }


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['pictures']
        widgets = {
            'product': forms.HiddenInput(),
            'picture': forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        }
