# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('umuco', '0007_auto_20160301_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, help_text='Partenair'),
            preserve_default=False,
        ),
    ]
