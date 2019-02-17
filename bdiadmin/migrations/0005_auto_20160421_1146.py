# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("bdiadmin", "0004_merge")]

    operations = [
        migrations.AlterField(
            model_name="colline",
            name="name",
            field=models.CharField(max_length=30, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="commune",
            name="name",
            field=models.CharField(unique=True, max_length=20, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="profileuser",
            name="telephone",
            field=models.CharField(
                blank=True,
                help_text="The telephone to contact you.",
                max_length=16,
                verbose_name="telephone",
                validators=[
                    django.core.validators.RegexValidator(
                        regex=b"^\\+?1?\\d{9,15}$",
                        message="Phone number in the format: '+999999999'. Up to 15 digits allowed.",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="name",
            field=models.CharField(unique=True, max_length=20, verbose_name="name"),
        ),
    ]
