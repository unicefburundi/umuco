# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0014_auto_20171024_1914")]

    operations = [
        migrations.AlterField(
            model_name="kindofsupport",
            name="support_name",
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
        )
    ]
