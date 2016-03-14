# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('bdiadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NawenuzeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_of_meeting', models.PositiveIntegerField(help_text='Number. Eg : For Monday put 1, Tuesday put 2, ...', null=True, verbose_name='Day of meeting', validators=[django.core.validators.MaxValueValidator(7)])),
                ('lamps_in_stock', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('cost_lamp', models.PositiveIntegerField(default=8000, null=True, blank=True)),
                ('cost_recharge', models.PositiveIntegerField(default=300, null=True, blank=True)),
                ('colline', models.OneToOneField(to='bdiadmin.Colline', help_text='Required')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('pass_word', models.CharField(default=b'12ab', max_length=12, editable=False)),
                ('partner', models.ForeignKey(help_text='Partenair focalt point ', to='bdiadmin.ProfileUser')),
            ],
            bases=('auth.group',),
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
                ('lamps_received', models.PositiveIntegerField(default=0, verbose_name='Received lamps')),
                ('date_received', models.DateField(default=django.utils.timezone.now, verbose_name='Date received')),
                ('group', models.ForeignKey(verbose_name='group', to='umuco.NawenuzeGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date submited')),
                ('date_updated', models.DateField(default=django.utils.timezone.now, verbose_name='Date refering to')),
                ('recharged_lamps', models.PositiveIntegerField(default=0, verbose_name='Recharged lamps')),
                ('sold_lamps', models.PositiveIntegerField(default=0, verbose_name='Sold Lamps')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Amount')),
                ('group', models.ForeignKey(verbose_name='group', to='umuco.NawenuzeGroup')),
            ],
        ),
    ]
