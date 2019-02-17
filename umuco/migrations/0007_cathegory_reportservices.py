# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0006_auto_20160707_1038")]

    operations = [
        migrations.CreateModel(
            name="Cathegory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("code", models.PositiveIntegerField(unique=True)),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Type of service"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReportServices",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "date_updated",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="Date of report"
                    ),
                ),
                ("beneficiary", models.PositiveIntegerField(default=0)),
                ("service", models.ForeignKey(to="umuco.Cathegory")),
            ],
        ),
    ]
