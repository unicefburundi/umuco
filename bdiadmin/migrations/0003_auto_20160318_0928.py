# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("bdiadmin", "0002_auto_20160317_0947")]

    operations = [
        migrations.AlterField(
            model_name="colline",
            name="name",
            field=models.CharField(max_length=30, verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="commune",
            name="name",
            field=models.CharField(unique=True, max_length=20, verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="profileuser",
            name="telephone",
            field=models.CharField(
                blank=True,
                help_text="Le t\xe9l\xe9phone pour vous contacter.",
                max_length=16,
                verbose_name="t\xe9l\xe9phone",
                validators=[
                    django.core.validators.RegexValidator(
                        regex=b"^\\+?1?\\d{9,15}$",
                        message="Numero de t\xe9l\xe9phone au format : '+999999999'.Jusqu'\xe0 15 chiffres permis.",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="name",
            field=models.CharField(unique=True, max_length=20, verbose_name="nom"),
        ),
    ]
