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
                ('name', models.CharField(default=b'Anonymous group', max_length=60, serialize=False, primary_key=True)),
                ('location', models.CharField(max_length=60, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhoneModel',
            fields=[
                ('phone_number', models.CharField(default=b'+999999999', max_length=15, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
            ],
            options={
            },
            bases=(models.Model,),
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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nawenuzegroup',
            name='phone',
            field=models.ManyToManyField(default=umuco.models.get_default_phone, to='umuco.PhoneModel', through='umuco.Report'),
            preserve_default=True,
        ),
    ]
