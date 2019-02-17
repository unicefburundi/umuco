# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0002_auto_20160321_1133")]

    operations = [
        migrations.AlterField(
            model_name="nawenuzegroup",
            name="cost_lamp",
            field=models.PositiveIntegerField(
                default=8000, null=True, verbose_name="cost lamp ", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="nawenuzegroup",
            name="cost_recharge",
            field=models.PositiveIntegerField(
                default=300, null=True, verbose_name="cost recharge", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="nawenuzegroup",
            name="lamps_in_stock",
            field=models.PositiveIntegerField(
                default=0, null=True, verbose_name="lamps in stock", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="pass_word",
            field=models.CharField(default=b"35ug", max_length=12, editable=False),
        ),
    ]
