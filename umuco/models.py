from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.validators import MaxValueValidator
from bdiadmin.models import *


class NawenuzeGroup(models.Model):
    colline = models.OneToOneField(Colline, help_text=_('Required'))
    day_of_meeting = models.PositiveIntegerField(verbose_name=_("Reporting day"), help_text=_('Number. Ex : For Monday put 1, Tuesday put 2, ...'), null=True, validators=[MaxValueValidator(7),])
    lamps_in_stock = models.PositiveIntegerField(verbose_name=_("lamps in stock"), default=0 , null=True, blank=True)
    cost_lamp = models.PositiveIntegerField(verbose_name=_("cost lamp "), default=8000 , null=True, blank=True)
    cost_recharge = models.PositiveIntegerField(verbose_name=_("cost recharge"), default=300 , null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.colline


class AnimateurSocial(models.Model):
    name = models.CharField(_('Name'), help_text=_('The name of the AS'), max_length=40)
    # The additional attributes we wish to include.
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number in the format: '+999999999'. Up to 15 digits allowed."))
    telephone = models.CharField(_('telephone'), validators=[phone_regex], blank=True, help_text=_('The telephone to contact you.'), max_length=16)
    groups = models.ManyToManyField(NawenuzeGroup, blank=True)

    def __unicode__(self):
        return u"%s" % self.name


class PhoneModel(models.Model):
    number = models.CharField(primary_key=True, max_length=15, verbose_name=_('phone number'), unique=True)
    group = models.ForeignKey(NawenuzeGroup, verbose_name=_('group'))
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.number


class Report(models.Model):
    """
    a model for a NaweNuze report
    """
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date submitted'))
    date_updated = models.DateField(verbose_name=_('Date of report'), default=timezone.now)
    recharged_lamps = models.PositiveIntegerField(default=0,verbose_name=_('Recharged lamps'))
    sold_lamps = models.PositiveIntegerField(_('Sold Lamps'), default=0)
    total_amount = models.PositiveIntegerField(default=0, verbose_name=_('total amount'))
    pl_amount = models.PositiveIntegerField(default=0, verbose_name=_('PL amount'))
    group = models.ForeignKey(NawenuzeGroup, verbose_name=_('group'))

    def __unicode__(self):
        return u'%s %s %s %s' % (self.date_updated, self.sold_lamps, self.recharged_lamps, self.total_amount)


class Reception(models.Model):
    """
    reception of lamps
    """
    group = models.ForeignKey(NawenuzeGroup, verbose_name=_('group'))
    lamps_received = models.PositiveIntegerField(default=0, verbose_name=_('Received lamps'))
    date_received = models.DateField(verbose_name=_('Date received'), default=timezone.now)

    def __unicode__(self):
        return u'%s %s %s' % (self.group, self.lamps_received, self.date_received)


class SupportReport(models.Model):
    kind_of_support = models.CharField(max_length=1, choices=settings.SERVICES, verbose_name=_('Type of service'), default="A")
    childred_supported = models.PositiveIntegerField(verbose_name=_('Children supported'), default=0)
    report = models.ForeignKey(Report)
    comment = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.kind_of_support, self.childred_supported)


class Organization(Group):
    pass_word = models.CharField(max_length=12, default=settings.PASSWORD, editable=False)
    partner = models.ForeignKey(ProfileUser, help_text=_('Partner focal point '))

    def __unicode__(self):
        return u'%s' % (self.partner.user.name)


class Temporaly(models.Model):
    text = models.CharField(max_length=500)
    colline = models.OneToOneField(Colline, help_text=_('Required'))
    day_of_meeting = models.PositiveIntegerField(verbose_name=_("Day of reporting"), help_text=_('Number. Ex : For Monday put 1, Tuesday put 2, ...'), null=True, validators=[MaxValueValidator(7), ])
    lamps_in_stock = models.PositiveIntegerField(default=0, null=True, blank=True)
    cost_lamp = models.PositiveIntegerField(default=8000, null=True, blank=True)
    cost_recharge = models.PositiveIntegerField(default=300, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.colline


class ReportSummary(Report):
    class Meta:
        proxy = True
        verbose_name = 'Report Summary'
        verbose_name_plural = 'Reports Summaries'
