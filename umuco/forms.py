from django import forms
from umuco.models import Report, NawenuzeGroup, PhoneModel
from authtools.forms import UserCreationForm
from django.forms import inlineformset_factory


class RaportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('recharged_lamps', 'sold_lamps', 'amount')
        exclude = ('group',)

class UserCreationForm(UserCreationForm):
    """
    A UserCreationForm with optional password inputs.
    """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

MAX_PHONENUMBER = 2
class NaweNuzeForm(forms.ModelForm):
    class Meta:
        model = NawenuzeGroup
        fields = ('province', 'commune', 'colline', 'day_of_meeting')

GroupFormset  = inlineformset_factory(NawenuzeGroup, PhoneModel, fields = ('number',), extra=MAX_PHONENUMBER)

