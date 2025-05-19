# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstudy', '0004_vote_method3'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='method4',
            field=models.IntegerField(default=0),
        ),
    ]
