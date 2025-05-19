# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstudy', '0003_auto_20181030_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='method3',
            field=models.IntegerField(default=0),
        ),
    ]
