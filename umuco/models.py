from django.db import models
from django.core.validators import RegexValidator

class PhoneModel(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], default= '+999999999')

    def __unicode__(self):
        return u'%s' % self.phone_number

class NawenuzeGroup(models.Model):
    name = models.CharField(max_length=60, default="Anonymous group")
    phone = models.ManyToManyField(PhoneModel, blank=True, null=True, related_name='nawenuzegroup')
    location = models.CharField(max_length=60, blank=True)

    def __unicode__(self):
        return u'%s' % self.name

def get_default_group():
    return NawenuzeGroup.objects.get_or_create(name="Anonymous Group")

class Report( models.Model):
    """
    a model for a NaweNuze report
    """
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date submited')
    date_updated = models.DateField(auto_now=True, verbose_name='Date updated')
    recharged_lamps = models.IntegerField(default=0,verbose_name='Recharged lamps')
    sold_lamps = models.IntegerField(default=0, verbose_name='Sold Lamps')
    amount = models.IntegerField(default=0, verbose_name='Amount')
    group = models.ForeignKey(NawenuzeGroup, default=get_default_group)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.date , self.sold_lamps, self.recharged_lamps, self.amount)

