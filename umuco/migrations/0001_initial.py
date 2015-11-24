# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umuco.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NawenuzeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commune', models.CharField(max_length=150, blank=True)),
                ('colline', models.CharField(max_length=150)),
                ('day_of_meeting', models.IntegerField(null=True, verbose_name=b'Number. Eg : For Monday put 1, Tuesday put 2, ...')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneModel',
            fields=[
                ('number', models.CharField(max_length=15, unique=True, serialize=False, primary_key=True)),
                ('group', models.ForeignKey(to='umuco.NawenuzeGroup')),
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
            ],
        ),
    ]
