# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0002_auto_20160119_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='nawenuzegroup',
            name='cost_lamp',
            field=models.IntegerField(default=8000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='nawenuzegroup',
            name='cost_recharge',
            field=models.IntegerField(default=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reception',
            name='date_received',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date received'),
        ),
    ]
