from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _

def get_default_group():
    return NawenuzeGroup.objects.get_or_create(name="Anonymous_Group")

def get_default_phone():
    return PhoneModel.objects.get_or_create(phone_number="+25712345678")

DAY_OF_THE_WEEK = {
    '0' : _(u'Monday'),
    '1' : _(u'Tuesday'),
    '2' : _(u'Wednesday'),
    '3' : _(u'Thursday'),
    '4' : _(u'Friday'),
    '5' : _(u'Saturday'),
    '6' : _(u'Sunday'),
}

class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length']=1
        super(DayOfTheWeekField,self).__init__(*args, **kwargs)


class PhoneModel(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{7,21}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(primary_key=True, max_length=15, unique=True, validators=[phone_regex], default= '+123456789')

    def __unicode__(self):
        return u'%s' % self.phone_number

class NawenuzeGroup(models.Model):
    name = models.CharField(unique=True, max_length=60, default="Anonymous_group")
    person = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=60, blank=True)
    day_of_gathering = DayOfTheWeekField(default='1', null=True, blank=True)
    province = models.CharField(unique=True,max_length=60, blank=True, null=True)
    commune = models.CharField(max_length=60, blank=True)
    colline = models.CharField(max_length=60, blank=True)

    def __unicode__(self):
        return u'%s' % self.name


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
    telephone = models.ForeignKey(PhoneModel, default=get_default_phone)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.date , self.sold_lamps, self.recharged_lamps, self.amount)

