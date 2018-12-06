# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="nawenuzegroup",
            name="colline",
            field=models.OneToOneField(to="bdiadmin.Colline", help_text="Obligatoire"),
        ),
        migrations.AlterField(
            model_name="nawenuzegroup",
            name="day_of_meeting",
            field=models.PositiveIntegerField(
                help_text="Nombre. Par exemple: Pour le lundi mettre 1, le mardi mettre 2, ...",
                null=True,
                verbose_name="Jour de la r\xe9union",
                validators=[django.core.validators.MaxValueValidator(7)],
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="partner",
            field=models.ForeignKey(
                help_text="Partenaire point focal", to="bdiadmin.ProfileUser"
            ),
        ),
        migrations.AlterField(
            model_name="phonemodel",
            name="group",
            field=models.ForeignKey(verbose_name="groupe", to="umuco.NawenuzeGroup"),
        ),
        migrations.AlterField(
            model_name="phonemodel",
            name="number",
            field=models.CharField(
                max_length=15,
                unique=True,
                serialize=False,
                verbose_name="num\xe9ro de t\xe9l\xe9phone",
                primary_key=True,
            ),
        ),
        migrations.AlterField(
            model_name="reception",
            name="date_received",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="Date de r\xe9ception"
            ),
        ),
        migrations.AlterField(
            model_name="reception",
            name="group",
            field=models.ForeignKey(verbose_name="groupe", to="umuco.NawenuzeGroup"),
        ),
        migrations.AlterField(
            model_name="reception",
            name="lamps_received",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Lampes re\xe7ues"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="amount",
            field=models.PositiveIntegerField(default=0, verbose_name="Montant"),
        ),
        migrations.AlterField(
            model_name="report",
            name="date",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Date de soumission"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="date_updated",
            field=models.DateField(
                default=django.utils.timezone.now,
                verbose_name="Date de r\xe9f\xe9rent \xe0",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="group",
            field=models.ForeignKey(verbose_name="groupe", to="umuco.NawenuzeGroup"),
        ),
        migrations.AlterField(
            model_name="report",
            name="recharged_lamps",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Lampes recharg\xe9es"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="sold_lamps",
            field=models.PositiveIntegerField(default=0, verbose_name="Lampes vendues"),
        ),
    ]
