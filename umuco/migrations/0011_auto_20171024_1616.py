# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('umuco', '0010_auto_20171024_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('childred_supported', models.PositiveIntegerField(verbose_name='Children supported')),
                ('comment', models.TextField()),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.RemoveField(
            model_name='reportservices',
            name='service',
        ),
        migrations.AlterModelOptions(
            name='kindofsupport',
            options={'verbose_name_plural': 'Kinds of support'},
        ),
        migrations.RemoveField(
            model_name='kindofsupport',
            name='code',
        ),
        migrations.RemoveField(
            model_name='kindofsupport',
            name='name',
        ),
        migrations.AddField(
            model_name='kindofsupport',
            name='support_name',
            field=models.CharField(default=1, max_length=50, verbose_name='Type of service'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ReportServices',
        ),
        migrations.AddField(
            model_name='supportreport',
            name='kind_of_support',
            field=models.ForeignKey(to='umuco.KindOfSupport'),
        ),
        migrations.AddField(
            model_name='supportreport',
            name='report',
            field=models.ForeignKey(to='umuco.Report'),
        ),
    ]
