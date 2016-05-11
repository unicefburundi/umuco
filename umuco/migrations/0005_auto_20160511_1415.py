# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0004_auto_20160422_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nawenuzegroup',
            name='day_of_meeting',
            field=models.PositiveIntegerField(help_text='Number. Eg : For Monday put 1, Tuesday put 2, ...', null=True, verbose_name='Reporting day', validators=[django.core.validators.MaxValueValidator(7)]),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_updated',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date submited'),
        ),
    ]
