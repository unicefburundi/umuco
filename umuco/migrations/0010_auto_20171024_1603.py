# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0009_auto_20171024_1547")]

    operations = [
        migrations.RenameModel(old_name="Category", new_name="KindOfSupport"),
        migrations.AlterModelOptions(
            name="kindofsupport", options={"verbose_name_plural": "Categories"}
        ),
        migrations.AlterModelOptions(
            name="reportsummary",
            options={
                "verbose_name": "Report Summary",
                "verbose_name_plural": "Reports Summaries",
            },
        ),
    ]
