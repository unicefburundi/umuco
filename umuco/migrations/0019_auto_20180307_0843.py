# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0018_animateursocial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animateursocial',
            name='groups',
            field=models.ManyToManyField(to='umuco.NawenuzeGroup', blank=True),
        ),
    ]
