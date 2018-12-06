# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0008_merge")]

    operations = [
        migrations.AlterField(
            model_name="nawenuzegroup",
            name="colline",
            field=models.OneToOneField(to="bdiadmin.Colline", help_text="Required"),
        ),
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
            model_name="organization",
            name="partner",
            field=models.ForeignKey(
                help_text="Partner focal point ", to="bdiadmin.ProfileUser"
            ),
        ),
        migrations.AlterField(
            model_name="phonemodel",
            name="group",
            field=models.ForeignKey(verbose_name="group", to="umuco.NawenuzeGroup"),
        ),
        migrations.AlterField(
            model_name="phonemodel",
            name="number",
            field=models.CharField(
                max_length=15,
                unique=True,
                serialize=False,
                verbose_name="phone number",
                primary_key=True,
            ),
        ),
        migrations.AlterField(
            model_name="reception",
            name="date_received",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="Date received"
            ),
        ),
        migrations.AlterField(
            model_name="reception",
            name="group",
            field=models.ForeignKey(verbose_name="group", to="umuco.NawenuzeGroup"),
        ),
        migrations.AlterField(
            model_name="reception",
            name="lamps_received",
            field=models.PositiveIntegerField(default=0, verbose_name="Received lamps"),
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
            model_name="report",
            name="group",
            field=models.ForeignKey(verbose_name="group", to="umuco.NawenuzeGroup"),
        ),
        migrations.AlterField(
            model_name="report",
            name="recharged_lamps",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Recharged lamps"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="sold_lamps",
            field=models.PositiveIntegerField(default=0, verbose_name="Sold Lamps"),
        ),
    ]
