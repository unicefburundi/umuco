# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import umuco.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NawenuzeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Anonymous_group', unique=True, max_length=60)),
                ('person', models.CharField(max_length=60, blank=True)),
                ('phone', models.CharField(max_length=15, blank=True)),
                ('location', models.CharField(max_length=60, blank=True)),
                ('day_of_gathering', umuco.models.DayOfTheWeekField(default=b'1', max_length=1, null=True, blank=True, choices=[(b'1', 'Monday'), (b'2', 'Tuesday'), (b'3', 'Wednesday'), (b'4', 'Thursday'), (b'5', 'Friday'), (b'6', 'Saturday'), (b'7', 'Sunday')])),
                ('province', models.CharField(max_length=60, unique=True, null=True, blank=True)),
                ('commune', models.CharField(max_length=60, blank=True)),
                ('colline', models.CharField(max_length=60, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneModel',
            fields=[
                ('phone_number', models.CharField(primary_key=True, default=b'+123456789', serialize=False, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{7,21}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")], unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date submited')),
                ('date_updated', models.DateField(auto_now=True, verbose_name=b'Date updated')),
                ('recharged_lamps', models.IntegerField(default=0, verbose_name=b'Recharged lamps')),
                ('sold_lamps', models.IntegerField(default=0, verbose_name=b'Sold Lamps')),
                ('amount', models.IntegerField(default=0, verbose_name=b'Amount')),
                ('group', models.ForeignKey(default=umuco.models.get_default_group, to='umuco.NawenuzeGroup')),
                ('telephone', models.ForeignKey(default=umuco.models.get_default_phone, to='umuco.PhoneModel')),
            ],
        ),
    ]
