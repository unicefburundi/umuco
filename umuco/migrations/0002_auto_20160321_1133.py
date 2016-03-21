# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0003_auto_20160321_1133'),
        ('umuco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temporaly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=500)),
                ('day_of_meeting', models.PositiveIntegerField(help_text='Number. Eg : For Monday put 1, Tuesday put 2, ...', null=True, verbose_name='Day of meeting', validators=[django.core.validators.MaxValueValidator(7)])),
                ('lamps_in_stock', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('cost_lamp', models.PositiveIntegerField(default=8000, null=True, blank=True)),
                ('cost_recharge', models.PositiveIntegerField(default=300, null=True, blank=True)),
                ('colline', models.OneToOneField(to='bdiadmin.Colline', help_text='Required')),
            ],
        ),
        migrations.AlterField(
            model_name='organization',
            name='partner',
            field=models.ForeignKey(help_text='Partner focal point ', to='bdiadmin.ProfileUser'),
        ),
    ]
