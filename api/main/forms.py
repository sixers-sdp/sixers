from django import forms
from main.models import Order, LocationUpdate, CafeMap


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'products', 'products_text', 'state']


class LocationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'] = forms.ChoiceField(
            choices=[(n, n) for n in CafeMap.objects.all().last().get_all_locations()]
        )

    class Meta:
        model = LocationUpdate
        fields = ['location']
