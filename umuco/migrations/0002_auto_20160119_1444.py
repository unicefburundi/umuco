# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nawenuzegroup',
            name='lamps_in_stock',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
