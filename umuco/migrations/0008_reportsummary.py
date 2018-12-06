# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0007_cathegory_reportservices")]

    operations = [
        migrations.CreateModel(
            name="ReportSummary",
            fields=[],
            options={
                "verbose_name": "Report Summary",
                "proxy": True,
                "verbose_name_plural": "Reports Summary",
            },
            bases=("umuco.report",),
        )
    ]
