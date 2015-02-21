# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('injira', '0002_raport'),
    ]

    operations = [
        migrations.AddField(
            model_name='raport',
            name='groupe',
            field=models.CharField(default=b'Anonymous group', max_length=60, blank=True),
            preserve_default=True,
        ),
    ]
