# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('umuco', '0003_auto_20160122_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='auth.Group')),
                ('pass_word', models.CharField(default=b'12ab', max_length=12)),
                ('number', models.CharField(max_length=15, unique=True, serialize=False, verbose_name='phone number', primary_key=True)),
            ],
            bases=('auth.group',),
        ),
    ]
