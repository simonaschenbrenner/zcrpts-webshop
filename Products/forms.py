from django import forms
from django.urls import reverse_lazy
from django.views.generic import UpdateView

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
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['title', 'text', 'rate']
        widgets = {
            'myuser': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'rate': forms.RadioSelect(choices=CHOICES),
        }


class EditReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = (
            'title',
            'text',
            'rate',
        )
        widgets = {
            'rate': forms.RadioSelect(choices=CHOICES),
        }

# class EditReviewForm(UpdateView):
#     model = Comment
#     fields = ['title', 'text', 'rate']
#     template_name_suffix = '_update_form'
#     success_url = reverse_lazy('product-detail')


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['pictures']
        widgets = {
            'product': forms.HiddenInput(),
            'picture': forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        }
