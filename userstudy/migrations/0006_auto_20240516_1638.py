# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstudy', '0005_vote_method4'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='method5',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vote',
            name='method6',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vote',
            name='method7',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vote',
            name='method8',
            field=models.IntegerField(default=0),
        ),
    ]
