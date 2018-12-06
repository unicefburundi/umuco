# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("umuco", "0017_merge")]

    operations = [
        migrations.CreateModel(
            name="AnimateurSocial",
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
                    "name",
                    models.CharField(
                        help_text="The name of the AS",
                        max_length=40,
                        verbose_name="Name",
                    ),
                ),
                (
                    "telephone",
                    models.CharField(
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
                ("groups", models.ManyToManyField(to="umuco.NawenuzeGroup")),
            ],
        )
    ]
