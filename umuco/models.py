from django.db import models
from django.utils.translation import ugettext as _
from django.utils.timezone import now

def get_default_group():
    return NawenuzeGroup.objects.get_or_create(colline="Anonymous_Group")


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


class NawenuzeGroup(models.Model):
    province = models.CharField(max_length=150, blank=True)
    commune = models.CharField(max_length=150, blank=True)
    colline = models.CharField(max_length=150)
    day_of_meeting = models.IntegerField(help_text='Number. Eg : For Monday put 1, Tuesday put 2, ...', null=True)

    def __unicode__(self):
        return u'%s' % self.colline

class PhoneModel(models.Model):
    number = models.CharField(primary_key=True, max_length=15, unique=True)
    group = models.ForeignKey(NawenuzeGroup)

    def __unicode__(self):
        return u'%s' % self.number


class Report( models.Model):
    """
    a model for a NaweNuze report
    """
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date submited')
    date_updated = models.DateField(verbose_name='Date refering to', default=now())
    recharged_lamps = models.IntegerField(default=0,verbose_name='Recharged lamps')
    sold_lamps = models.IntegerField(default=0, verbose_name='Sold Lamps')
    amount = models.IntegerField(default=0, verbose_name='Amount')
    group = models.ForeignKey(NawenuzeGroup, default=get_default_group)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.date_updated , self.sold_lamps, self.recharged_lamps, self.amount)
