# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0013_auto_20171024_1912")]

    operations = [
        migrations.AlterField(
            model_name="supportreport",
            name="kind_of_support",
            field=models.ForeignKey(blank=True, to="umuco.KindOfSupport", null=True),
        )
    ]
