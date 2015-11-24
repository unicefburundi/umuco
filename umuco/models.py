from django.db import models
from models import *

def get_default_group():
    return NawenuzeGroup.objects.get_or_create(colline="Anonymous_Group")

def get_default_phone():
    return PhoneModel.objects.get_or_create(number="+25712345678")

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
    date_updated = models.DateField(auto_now=True, verbose_name='Date updated')
    recharged_lamps = models.IntegerField(default=0,verbose_name='Recharged lamps')
    sold_lamps = models.IntegerField(default=0, verbose_name='Sold Lamps')
    amount = models.IntegerField(default=0, verbose_name='Amount')
    group = models.ForeignKey(NawenuzeGroup, default=get_default_group)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.date_updated , self.sold_lamps, self.recharged_lamps, self.amount)
