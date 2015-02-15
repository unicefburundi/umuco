from django import forms
from injira.models import Contact

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('nom', 'mail', 'staff')

class ContactEmbeded(forms.Form):
    url = forms.URLField()