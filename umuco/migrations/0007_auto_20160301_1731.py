# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0006_organization_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nawenuzegroup',
            name='colline',
            field=models.CharField(help_text='Required', unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='nawenuzegroup',
            name='commune',
            field=models.CharField(help_text='Required', max_length=150, blank=True),
        ),
    ]
