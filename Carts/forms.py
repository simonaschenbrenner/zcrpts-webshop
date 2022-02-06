from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['credit_card_number', 'expiry_date', 'cvc']
        widgets = {
            'myuser': forms.HiddenInput(),
        }
