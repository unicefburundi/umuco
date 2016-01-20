# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umuco.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NawenuzeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('province', models.CharField(max_length=150, blank=True)),
                ('commune', models.CharField(max_length=150, blank=True)),
                ('colline', models.CharField(max_length=150)),
                ('day_of_meeting', models.IntegerField(help_text='Number. Eg : For Monday put 1, Tuesday put 2, ...', null=True, verbose_name='Day of meeting')),
                ('lamps_in_stock', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneModel',
            fields=[
                ('number', models.CharField(max_length=15, unique=True, serialize=False, verbose_name='phone number', primary_key=True)),
                ('group', models.ForeignKey(verbose_name='group', to='umuco.NawenuzeGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lamps_received', models.IntegerField(default=0, verbose_name='Received lamps')),
                ('date_received', models.DateField(default=django.utils.timezone.now, verbose_name='Date refering to')),
                ('group', models.ForeignKey(default=umuco.models.get_default_group, verbose_name='group', to='umuco.NawenuzeGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date submited')),
                ('date_updated', models.DateField(default=django.utils.timezone.now, verbose_name='Date refering to')),
                ('recharged_lamps', models.IntegerField(default=0, verbose_name='Recharged lamps')),
                ('sold_lamps', models.IntegerField(default=0, verbose_name='Sold Lamps')),
                ('amount', models.IntegerField(default=0, verbose_name='Amount')),
                ('group', models.ForeignKey(default=umuco.models.get_default_group, verbose_name='group', to='umuco.NawenuzeGroup')),
            ],
        ),
    ]
