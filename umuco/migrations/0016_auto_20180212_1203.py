# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0015_auto_20180212_1136")]

    operations = [
        migrations.AlterField(
            model_name="supportreport",
            name="kind_of_support",
            field=models.CharField(
                default=b"A",
                max_length=1,
                verbose_name="Type of service",
                choices=[
                    (b"A", "Medical Assistance"),
                    (b"B", "School fees"),
                    (b"C", "Legal Assistance"),
                    (b"D", "Orphans Assistance"),
                    (b"E", "Other Assistances"),
                ],
            ),
        ),
        migrations.DeleteModel(name="KindOfSupport"),
    ]
