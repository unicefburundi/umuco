from django import forms
from umuco.models import Report, NawenuzeGroup, PhoneModel
from authtools.forms import UserCreationForm
from django.forms import inlineformset_factory
from bdiadmin.models import *
from django.utils.translation import ugettext_lazy as _


def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield

class RaportForm(forms.ModelForm):
    formfield_callback = make_custom_datefield

    class Meta:
        model = Report
        fields = ('recharged_lamps', 'sold_lamps', 'total_amount', 'date_updated', 'group', 'pl_amount')

class PhoneModelForm(forms.ModelForm):
    class Meta:
        model = PhoneModel
        fields = ('group', 'number',  )

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
            raise forms.ValidationError(_("Fill out both fields"))
        return password2

MAX_PHONENUMBER = 2

DAYS_OF_WEEK = (
    (1, _('Monday')),
    (2, _('Tuesday')),
    (3, _('Wednesday')),
    (4, _('Thursday')),
    (5, _('Friday')),
    (6, _('Saturday')),
    (7, _('Sunday')),
)

class NaweNuzeForm(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.all())
    commune = forms.ChoiceField(widget = forms.Select(), required=False, choices=([('','------'), ]))
    colline = forms.ChoiceField(widget = forms.Select(), required=False, choices=([('','------'), ]))
    day_of_meeting = forms.ChoiceField(label=_('Day of reporting'), widget = forms.Select(), required=False, choices=DAYS_OF_WEEK)

    class Meta:
        model = NawenuzeGroup
        fields = ('colline', 'day_of_meeting')


    def is_valid(self):
        valid = super(NaweNuzeForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        try:
            self.cleaned_data['colline'] = Colline.objects.get(id=int(self.data.get('colline')))
        except:
            self._errors['colline'] = "Colline doesn't exist"
            return False

        # dangerous hack
        if self.data.get('colline') and 'colline' in self.errors:
            del self._errors['colline']

        # dangerous hack
        if self.data.get('commune') and 'commune' in self.errors:
            del self._errors['commune']

        return True

    def clean(self):
        self.cleaned_data = super(NaweNuzeForm, self).clean()

        try:
            self.cleaned_data['colline'] = Colline.objects.get(id=int(self.data.get('colline')))
        except:
            self._errors['colline'] = "Colline doesn't exist"
            return False

        # dangerous hack
        if self.data.get('colline') and 'colline' in self.errors:
            del self._errors['colline']

        # dangerous hack
        if self.data.get('commune') and 'commune' in self.errors:
            del self._errors['commune']

        return self.cleaned_data




GroupFormset  = inlineformset_factory(NawenuzeGroup, PhoneModel, fields = ('number',), extra=MAX_PHONENUMBER)

