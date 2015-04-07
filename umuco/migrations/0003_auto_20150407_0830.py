# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0002_auto_20150404_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nawenuzegroup',
            name='name',
            field=models.CharField(default=b'Anonymous_group', max_length=60, serialize=False, primary_key=True),
        ),
    ]
