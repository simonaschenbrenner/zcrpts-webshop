from django import forms
from .models import Product, Comment


CHOICES = (
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
)


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = [
            'title',
            'version',
            'short_description',
            'long_description',
            'pdf',
            'logo',
            'screenshot',
            'featured',
            'operating_system',
            'language',
            'tested_with',
            'script',
            'price',
        ]
        widgets = {
            'myuser': forms.HiddenInput()
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['title', 'text', 'rating']
        widgets = {
            'myuser': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'rating': forms.RadioSelect(choices=CHOICES),
        }


class EditReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = (
            'title',
            'text',
            'rating',
        )
        widgets = {
            'rating': forms.RadioSelect(choices=CHOICES),
        }


class SearchForm(forms.Form):
    search_term = forms.CharField(
        label='search_term',
        max_length=50,
        required=False)
    min_stars = forms.ChoiceField(
        label='min_stars',
        choices=CHOICES,
        widget=forms.Select,
        required=False)
