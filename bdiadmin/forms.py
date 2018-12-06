from bdiadmin.models import *
from django import forms


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ("name", "code")


class CommuneForm(forms.ModelForm):
    class Meta:
        model = Commune
        fields = ("province", "name", "code")


class CollineForm(forms.ModelForm):
    class Meta:
        model = Colline
        fields = ("commune", "name", "code")
