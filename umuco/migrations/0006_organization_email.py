# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0005_auto_20160122_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='email',
            field=models.EmailField(max_length=100, blank=True),
        ),
    ]
