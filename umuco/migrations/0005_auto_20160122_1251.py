# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0004_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='pass_word',
            field=models.CharField(default=b'12ab', max_length=12, editable=False),
        ),
    ]
