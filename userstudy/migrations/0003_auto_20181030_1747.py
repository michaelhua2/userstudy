# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstudy', '0002_auto_20170728_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='content',
            new_name='sceneId',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='method3',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='method4',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='method5',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='style',
        ),
    ]
