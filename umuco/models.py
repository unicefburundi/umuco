from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings

def get_default_group():
    return NawenuzeGroup.objects.get_or_create(colline=_("Anonymous_Group"))


class NawenuzeGroup(models.Model):
    province = models.CharField(max_length=150, blank=True)
    commune = models.CharField(max_length=150, blank=True)
    colline = models.CharField(max_length=150)
    day_of_meeting = models.IntegerField(verbose_name=_("Day of meeting"), help_text=_('Number. Eg : For Monday put 1, Tuesday put 2, ...'), null=True)
    lamps_in_stock = models.IntegerField(default=0 , null=True, blank=True)
    cost_lamp = models.IntegerField(default=8000 , null=True, blank=True)
    cost_recharge = models.IntegerField(default=300 , null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.colline

class PhoneModel(models.Model):
    number = models.CharField(primary_key=True, max_length=15, verbose_name=_('phone number'), unique=True)
    group = models.ForeignKey(NawenuzeGroup, verbose_name=_('group'))

    def __unicode__(self):
        return u'%s' % self.number


class Report( models.Model):
    """
    a model for a NaweNuze report
    """
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date submited'))
    date_updated = models.DateField(verbose_name=_('Date refering to'), default=timezone.now)
    recharged_lamps = models.IntegerField(default=0,verbose_name=_('Recharged lamps'))
    sold_lamps = models.IntegerField(default=0, verbose_name=_('Sold Lamps'))
    amount = models.IntegerField(default=0, verbose_name=_('Amount'))
    group = models.ForeignKey(NawenuzeGroup, verbose_name=_('group'), default=get_default_group)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.date_updated , self.sold_lamps, self.recharged_lamps, self.amount)

class Reception(models.Model):
    """
    reception of lamps
    """
    group = models.ForeignKey(NawenuzeGroup, verbose_name=_('group'), default=get_default_group)
    lamps_received = models.IntegerField(default=0, verbose_name=_('Received lamps'))
    date_received = models.DateField(verbose_name=_('Date received'), default=timezone.now)

    def __unicode__(self):
        return u'%s %s %s' % (self.group , self.lamps_received, self.date_received)

class Organization(Group):
    pass_word = models.CharField(max_length=12, default=settings.PASSWORD, editable=False)
    number = models.CharField(primary_key=True, max_length=15, verbose_name=_('phone number'), unique=True)

    def __unicode__(self):
        return u'%s %s' % (self.name , self.number)