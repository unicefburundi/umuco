# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('umuco', '0008_organization_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='email',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='number',
        ),
        migrations.AlterField(
            model_name='organization',
            name='group_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='user',
            field=models.ForeignKey(help_text='Partenair focalt point ', to=settings.AUTH_USER_MODEL),
        ),
    ]
