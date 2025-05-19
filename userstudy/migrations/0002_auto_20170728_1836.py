# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstudy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='age',
        ),
        migrations.RemoveField(
            model_name='people',
            name='exp',
        ),
        migrations.RemoveField(
            model_name='people',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='check',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='img_id',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='reason',
        ),
        migrations.AddField(
            model_name='vote',
            name='content',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vote',
            name='method3',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vote',
            name='method4',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vote',
            name='method5',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vote',
            name='style',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
