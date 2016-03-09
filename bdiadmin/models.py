from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.conf import settings


class ProfileUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # The additional attributes we wish to include.
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    telephone = models.CharField(_('telephone'), validators=[phone_regex], blank=True, help_text=_('The telephone to contact you.'), max_length=16)

class Province(models.Model):
    '''In this model, we will store burundi provinces'''
    name = models.CharField(_('name'),unique=True, max_length=20)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('province_detail', kwargs={'pk': self.id})
        return self.id

    class Meta:
        ordering = ('name',)

class Commune(models.Model):
    '''In this model, we will store burundi communes'''
    province = models.ForeignKey(Province)
    name = models.CharField(_('name'),unique=True, max_length=20)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('province_detail', kwargs={'pk': self.id})
        return self.id

    class Meta:
        ordering = ('name',)

class Colline(models.Model):
    '''In this model, we will store burundi colline'''
    commune = models.ForeignKey(Commune)
    name = models.CharField(_('name'),unique=True, max_length=20)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('province_detail', kwargs={'pk': self.id})
        return self.id

    class Meta:
        ordering = ('name',)


