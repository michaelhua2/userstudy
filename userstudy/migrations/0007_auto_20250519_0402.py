# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstudy', '0006_auto_20240516_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='is_colorblind',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='people',
            name='code',
            field=models.CharField(max_length=20, default=''),
        ),
        migrations.AlterField(
            model_name='people',
            name='comment',
            field=models.TextField(default=''),
        ),
    ]
