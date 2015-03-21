from django import forms
from umuco.models import Report


class RaportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('recharged_lamps', 'sold_lamps', 'amount')