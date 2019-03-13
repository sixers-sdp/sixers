from django import forms
from main.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = []

