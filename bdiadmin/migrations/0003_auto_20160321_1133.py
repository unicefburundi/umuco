# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("bdiadmin", "0002_auto_20160317_0947")]

    operations = [
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
        )
    ]
