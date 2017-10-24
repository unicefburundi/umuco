# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0011_auto_20171024_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportreport',
            name='group',
        ),
        migrations.AlterField(
            model_name='supportreport',
            name='comment',
            field=models.TextField(null=True, blank=True),
        ),
    ]
