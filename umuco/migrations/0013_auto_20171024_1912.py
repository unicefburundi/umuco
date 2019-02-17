# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0012_auto_20171024_1714")]

    operations = [
        migrations.AlterField(
            model_name="kindofsupport",
            name="support_name",
            field=models.CharField(
                max_length=50, verbose_name="Type of service", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="supportreport",
            name="childred_supported",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Children supported"
            ),
        ),
    ]
