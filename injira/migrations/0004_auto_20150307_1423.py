# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('injira', '0003_raport_groupe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raport',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
    ]
