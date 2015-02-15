from django import forms
from injira.models import Contact, Raport

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('nom', 'mail', 'staff')

class ContactEmbeded(forms.Form):
    url = forms.URLField()

class RaportForm(forms.ModelForm):
    class Meta:
        model = Raport
        fields = ('lampes_rechargees', 'lampes_vendues', 'montant')