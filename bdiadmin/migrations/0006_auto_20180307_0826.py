# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdiadmin', '0005_auto_20160421_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colline',
            name='code',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='commune',
            name='code',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='province',
            name='code',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
