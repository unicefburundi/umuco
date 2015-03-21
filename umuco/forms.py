from django import forms
from umuco.models import Raport


class RaportForm(forms.ModelForm):
    class Meta:
        model = Raport
        fields = ('lampes_rechargees', 'lampes_vendues', 'montant')