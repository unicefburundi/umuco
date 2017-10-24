# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0008_reportsummary'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cathegory',
            new_name='Category',
        ),
    ]
