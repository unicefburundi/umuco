# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0005_auto_20160511_1415")]

    operations = [
        migrations.AlterField(
            model_name="nawenuzegroup",
            name="day_of_meeting",
            field=models.PositiveIntegerField(
                help_text="Number. Ex : For Monday put 1, Tuesday put 2, ...",
                null=True,
                verbose_name="Reporting day",
                validators=[django.core.validators.MaxValueValidator(7)],
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="date",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Date submitted"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="date_updated",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="Date of report"
            ),
        ),
        migrations.AlterField(
            model_name="temporaly",
            name="day_of_meeting",
            field=models.PositiveIntegerField(
                help_text="Number. Ex : For Monday put 1, Tuesday put 2, ...",
                null=True,
                verbose_name="Day of reporting",
                validators=[django.core.validators.MaxValueValidator(7)],
            ),
        ),
    ]
