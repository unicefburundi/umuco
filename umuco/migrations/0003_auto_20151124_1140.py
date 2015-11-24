# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0002_nawenuzegroup_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nawenuzegroup',
            name='day_of_meeting',
            field=models.IntegerField(help_text=b'Number. Eg : For Monday put 1, Tuesday put 2, ...', null=True),
        ),
    ]
