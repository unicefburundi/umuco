# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0003_auto_20160330_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='amount',
        ),
        migrations.AddField(
            model_name='report',
            name='pl_amount',
            field=models.PositiveIntegerField(default=0, verbose_name='PL amount'),
        ),
        migrations.AddField(
            model_name='report',
            name='total_amount',
            field=models.PositiveIntegerField(default=0, verbose_name='total amount'),
        ),
    ]
