# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0019_auto_20180307_0843")]

    operations = [
        migrations.AddField(
            model_name="phonemodel",
            name="is_active",
            field=models.BooleanField(default=False),
        )
    ]
